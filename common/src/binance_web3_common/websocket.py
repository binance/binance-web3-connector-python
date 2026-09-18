import asyncio
import logging
import requests

from typing import Optional, Union
from urllib.parse import quote

from binance_common.signature import Signers
from binance_common.websocket import (
    RequestStream,
    RequestStreamHandle,
    WebSocketConnection,
    WebSocketStreamBase as WebSocketStreamsBaseCommon,
)

from binance_web3_common.configuration import (
    ConfigurationRestAPI,
    ConfigurationWebSocketStreams,
)
from binance_web3_common.constants import (
    WEB3_WALLET_REST_API_PROD_URL,
    WEB3_WALLET_WS_STREAMS_PROD_URL,
    WEB3_WALLET_WS_STREAMS_TOKEN_ENDPOINT,
    WS_STREAMS_TOKEN_RENEWAL_SECONDS,
)
from binance_web3_common.utils import send_request

# Connections, subscriptions and reconnection are handled by `binance_common`.
# Its stream primitives are re-exported so the generated connector keeps a single
# import site.
__all__ = [
    "RequestStream",
    "RequestStreamHandle",
    "WebSocketConnection",
    "WebSocketStreamBase",
]


class WebSocketStreamBase(WebSocketStreamsBaseCommon):
    """WebSocket Streams client for the Binance Web3 Wallet API.

    Adds stream authentication on top of the shared `binance_common` streams
    client: every connection carries an auth token appended to the WebSocket URL
    as a `token` query parameter. Two modes are supported:

    - Managed token (`api_key` supplied): a token is fetched from the REST API on
      connect, reused on every reconnect, and renewed every 6 days, which keeps a
      24-hour margin inside its 7-day validity.
    - Caller-supplied token (`ws_token` supplied): the given token is used as is.
      No REST call is made and no renewal is scheduled.
    """

    def __init__(
        self,
        configuration: ConfigurationWebSocketStreams,
        id_strict_int: Optional[bool] = False,
        url_paths: Optional[str] = None,
    ):
        """Initialize the WebSocketStreamBase class.

        Args:
            configuration (ConfigurationWebSocketStreams): Configuration object.
            id_strict_int (Optional[bool]): Whether to use strict integer IDs.
            url_paths (Optional[str]): URL paths for the WebSocket connection.
        """

        if not configuration.stream_url:
            configuration.stream_url = WEB3_WALLET_WS_STREAMS_PROD_URL

        super().__init__(configuration, id_strict_int, url_paths)

        self._token: Optional[str] = None
        self._user_token = configuration.ws_token
        self._token_endpoint = (
            configuration.ws_token_endpoint or WEB3_WALLET_WS_STREAMS_TOKEN_ENDPOINT
        )
        self._token_renewal_task: Optional[asyncio.Task] = None
        self._rest_session: Optional[requests.Session] = None
        self._rest_configuration = (
            ConfigurationRestAPI(
                api_key=configuration.api_key,
                api_secret=configuration.api_secret,
                private_key=configuration.private_key,
                private_key_passphrase=configuration.private_key_passphrase,
                base_path=configuration.base_path or WEB3_WALLET_REST_API_PROD_URL,
                timeout=10000,
            )
            if configuration.api_key is not None
            else None
        )
        self._signer = (
            Signers.get_signer(
                configuration.private_key, configuration.private_key_passphrase
            )
            if configuration.private_key is not None
            else None
        )

    async def create_connection(self):
        """Authenticate the stream, then create a WebSocket connection.

        Returns:
            WebSocketConnection: The created WebSocket connection.

        Raises:
            ValueError: If neither `ws_token` nor `api_key` is configured, or if
                the REST API did not return an auth token.
        """

        await self._authenticate()

        return await super().create_connection()

    async def init_connection(
        self,
        url,
        configuration: ConfigurationWebSocketStreams,
        url_path: Optional[str] = None,
        ws_id: Optional[Union[str, int]] = None,
    ):
        """Initialize a WebSocket connection carrying the current auth token.

        Called both on the initial connection and on every reconnect, so the
        token held in memory is reused without fetching a new one.

        Args:
            url (str): WebSocket URL.
            configuration (ConfigurationWebSocketStreams): Configuration object.
            url_path (Optional[str]): Optional URL path for the connection.
            ws_id (Optional[Union[str, int]]): Optional WebSocket ID for the connection.
        """

        return await super().init_connection(
            self._append_token(url), configuration, url_path, ws_id
        )

    async def close_connection(
        self,
        connection: Optional[WebSocketConnection] = None,
        close_session: bool = True,
    ):
        """Close the WebSocket connection, stopping token renewal.

        Args:
            connection (Optional[WebSocketConnection]): WebSocket connection object to close.
                When omitted every connection is closed and token renewal stops.
            close_session (bool): Whether to close the aiohttp session.
        """

        if connection is None:
            self._cancel_token_renewal()
            self._close_rest_session()

        await super().close_connection(connection, close_session)

    async def _authenticate(self) -> None:
        """Obtain the auth token every stream connection is opened with.

        Raises:
            ValueError: If neither `ws_token` nor `api_key` is configured.
        """

        if self._user_token is not None:
            self._token = self._user_token
            return

        if self._rest_configuration is None:
            raise ValueError(
                "WebSocketStreamBase: 'api_key' is required when 'ws_token' is "
                "not provided."
            )

        self._token = await self._fetch_token()
        self._schedule_token_renewal()

    def _append_token(self, url: str) -> str:
        """Append the current auth token to a WebSocket URL.

        Args:
            url (str): The WebSocket URL to authenticate.

        Returns:
            str: The URL with a `token` query parameter, or the URL unchanged
                when no token has been obtained.
        """

        if not self._token:
            return url

        separator = "&" if "?" in url else "?"
        return f"{url}{separator}token={quote(str(self._token), safe='')}"

    async def _fetch_token(self) -> str:
        """Fetch a new auth token from the REST API.

        Returns:
            str: The fetched auth token.

        Raises:
            ValueError: If the response did not include a token.
        """

        if self._rest_session is None:
            self._rest_session = requests.Session()

        def request():
            return send_request(
                self._rest_session,
                self._rest_configuration,
                method="GET",
                path=self._token_endpoint,
                payload={},
                is_signed=True,
                signer=self._signer,
                web3_headers={},
            ).data()

        payload = await asyncio.to_thread(request)

        data = payload.get("data") if isinstance(payload, dict) else None
        token = data.get("token") if isinstance(data, dict) else None

        if not token:
            raise ValueError(
                "WebSocketStreamBase: failed to obtain a WebSocket auth token — "
                "the REST API response did not include a token field."
            )

        return token

    def _schedule_token_renewal(self) -> None:
        """Start renewing the auth token every `WS_STREAMS_TOKEN_RENEWAL_SECONDS`."""

        self._cancel_token_renewal()
        self._token_renewal_task = asyncio.create_task(self._renew_token_forever())

    async def _renew_token_forever(self) -> None:
        """Renew the auth token on a fixed cadence for as long as it is alive.

        A failed renewal is logged and retried on the next tick, so the cadence
        never stops while the connection is up.
        """

        while True:
            await asyncio.sleep(WS_STREAMS_TOKEN_RENEWAL_SECONDS)

            try:
                self._token = await self._fetch_token()
                await self._reconnect_with_new_token()
            except asyncio.CancelledError:
                raise
            except Exception as e:
                logging.error(f"WebSocket auth token renewal failed: {e}")

    async def _reconnect_with_new_token(self) -> None:
        """Reconnect every live connection so it carries the renewed token."""

        for connection in list(self.connections):
            if connection.close_initiated:
                continue

            await self.reconnect(connection, self.configuration)

    def _cancel_token_renewal(self) -> None:
        """Stop the token renewal, if one is scheduled."""

        task = self._token_renewal_task
        self._token_renewal_task = None

        if task is not None and not task.done():
            task.cancel()

    def _close_rest_session(self) -> None:
        """Close the HTTP session used to fetch auth tokens, if one was opened."""

        if self._rest_session is not None:
            self._rest_session.close()
            self._rest_session = None
