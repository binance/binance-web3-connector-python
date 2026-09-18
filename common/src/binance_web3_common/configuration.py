import ssl

from typing import Optional, Dict, Union, List

from binance_common.configuration import (
    ConfigurationRestAPI as ConfigurationRestAPIBase,
    ConfigurationWebSocketStreams as ConfigurationWebSocketStreamsBase,
)
from binance_common.headers import parse_custom_headers

from binance_web3_common.constants import (
    DEFAULT_RECONNECT_ATTEMPTS,
    WebsocketMode,
)

__all__ = ["ConfigurationRestAPI", "ConfigurationWebSocketStreams"]


class ConfigurationRestAPI(ConfigurationRestAPIBase):
    """
    Configuration for the Binance Web3 Wallet REST API client.

    Everything but the authentication headers is inherited from
    `binance_common`. The Web3 Wallet API sends the API key in `X-OC-APIKEY`
    instead of `X-MBX-APIKEY`, and expects a JSON content type.
    """

    def __init__(
        self,
        *args,
        custom_headers: Optional[dict[str, Union[str, List[str]]]] = None,
        **kwargs,
    ):
        """
        Initialize the API configuration.

        Every argument is forwarded to `binance_common.configuration.ConfigurationRestAPI`.

        Args:
            custom_headers (Optional[dict[str, Union[str, List[str]]]]): Custom REST headers (default: {}).
        """

        super().__init__(*args, custom_headers=custom_headers, **kwargs)

        self.base_headers = {
            **parse_custom_headers(custom_headers if custom_headers else {}),
            "Content-Type": "application/json",
            "X-OC-APIKEY": str(self.api_key) if self.api_key else "",
        }


class ConfigurationWebSocketStreams(ConfigurationWebSocketStreamsBase):
    """
    Configuration for the Binance Web3 Wallet Websocket Stream client.

    The connection settings are inherited from `binance_common`. This class adds
    the credentials and the endpoint used to obtain the stream auth token, plus
    the option to supply a token directly.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        private_key: Optional[Union[bytes, str]] = None,
        private_key_passphrase: Optional[str] = None,
        stream_url: Optional[str] = None,
        base_path: Optional[str] = None,
        ws_token: Optional[str] = None,
        ws_token_endpoint: Optional[str] = None,
        reconnect_delay: int = 5000,
        reconnect_attempts: int = DEFAULT_RECONNECT_ATTEMPTS,
        compression: int = 0,
        proxy: Optional[Dict[str, Union[str, int, Dict[str, str]]]] = None,
        mode: WebsocketMode = WebsocketMode.SINGLE,
        pool_size: int = 2,
        https_agent: Optional[ssl.SSLContext] = None,
    ):
        """
        Initialize the Websocket Stream configuration.

        Args:
            api_key (Optional[str]): API key used to fetch the stream auth token (default: None).
            api_secret (Optional[str]): API secret used to sign the token request (default: None).
            private_key (Optional[Union[bytes, str]]): Private key used to sign the token request (default: None).
            private_key_passphrase (Optional[str]): Passphrase for private key (default: None).
            stream_url (Optional[str]): Base WebSocket Stream URL (default: None).
            base_path (Optional[str]): Base REST API URL used to fetch the stream
                auth token (default: None).
            ws_token (Optional[str]): A WebSocket auth token to use as is. When
                given, no token is fetched and none is renewed (default: None).
            ws_token_endpoint (Optional[str]): REST path the auth token is
                fetched from (default: None).
            reconnect_delay (int): Delay (ms) between reconnections (default: 5000).
            reconnect_attempts (int): How many times to retry a failed reconnect
                before giving up on the connection. Must be between 1 and 10
                (default: 3).
            compression (int): Compression level (default: 0).
            proxy (Optional[Dict[str, Union[str, int, Dict[str, str]]]]): Proxy settings (default: None).
            mode (WebsocketMode): WebSocket mode ("single" or "pool") (default: "single").
            pool_size (int): Number of WebSocket connections in pool (default: 2).
            https_agent (Optional[ssl.SSLContext]): Custom HTTPS Agent (default: None).

        Raises:
            ValueError: If `reconnect_attempts` is outside the supported range.
        """

        # The Web3 Wallet streams do not support a time unit, so it is not a
        # constructor argument and stays unset on the inherited configuration.
        super().__init__(
            stream_url=stream_url,
            reconnect_delay=reconnect_delay,
            reconnect_attempts=reconnect_attempts,
            compression=compression,
            proxy=proxy,
            mode=mode,
            pool_size=pool_size,
            https_agent=https_agent,
        )

        self.api_key = api_key
        self.api_secret = api_secret
        self.private_key = private_key
        self.private_key_passphrase = private_key_passphrase
        self.base_path = base_path
        self.ws_token = ws_token
        self.ws_token_endpoint = ws_token_endpoint
