import asyncio
import logging
import pytest_asyncio
import pytest

from collections import defaultdict
from unittest.mock import AsyncMock, MagicMock, patch
from types import SimpleNamespace

from binance_common.websocket import WebSocketStreamBase as WebSocketStreamsBaseCommon

from binance_web3_common.configuration import ConfigurationWebSocketStreams
from binance_web3_common.constants import (
    WEB3_WALLET_REST_API_PROD_URL,
    WEB3_WALLET_WS_STREAMS_PROD_URL,
    WEB3_WALLET_WS_STREAMS_TOKEN_ENDPOINT,
    WS_STREAMS_TOKEN_RENEWAL_SECONDS,
)
from binance_web3_common.websocket import WebSocketStreamBase


# ========== Fixtures ==========
@pytest.fixture
def mock_websocket():
    ws = AsyncMock()
    ws.__aiter__.return_value = []
    ws._response = MagicMock()
    return ws


@pytest.fixture
def mock_connection():
    conn = MagicMock()
    conn.id = 1
    conn.reconnect = False
    conn.websocket = AsyncMock()
    conn.stream_callback_map = {}
    conn.connection_callback_map = defaultdict(list)
    conn.response_types = {}
    conn.is_open = True
    conn.close_initiated = False
    conn.scheduled_reconnect_task = None
    return conn


@pytest_asyncio.fixture(autouse=True)
async def cleanup_after_test():
    """Cleanup after each test to ensure no lingering tasks."""
    yield
    current_task = asyncio.current_task()
    tasks = [t for t in asyncio.all_tasks() if t is not current_task]
    for task in tasks:
        task.cancel()
    await asyncio.sleep(0.1)


# ========== Stream authentication tests ==========
#
# Connections, subscriptions and reconnection come from `binance_common` and are
# tested there. These tests only cover what `binance_web3_common` adds: the
# stream auth token.


class TestWebSocketStreamBaseAuth:

    @staticmethod
    def _configuration(**overrides):
        params = {
            "stream_url": "wss://test.com/ws",
            "reconnect_delay": 0,
            "reconnect_attempts": 1,
        }
        params.update(overrides)
        return ConfigurationWebSocketStreams(**params)

    def test_defaults_to_the_production_stream_url(self):
        configuration = ConfigurationWebSocketStreams(ws_token="test-token")

        WebSocketStreamBase(configuration)

        assert configuration.stream_url == f"{WEB3_WALLET_WS_STREAMS_PROD_URL}/stream"

    def test_append_token_uses_the_existing_query_string(self):
        stream = WebSocketStreamBase(self._configuration(ws_token="test-token"))
        stream._token = "test-token"

        assert (
            stream._append_token("wss://test.com/ws/stream?other=1")
            == "wss://test.com/ws/stream?other=1&token=test-token"
        )

    def test_append_token_without_a_token_leaves_the_url_alone(self):
        stream = WebSocketStreamBase(self._configuration(ws_token="test-token"))

        assert stream._append_token("wss://test.com/ws/stream") == (
            "wss://test.com/ws/stream"
        )

    @pytest.mark.asyncio
    @patch("binance_web3_common.websocket.send_request")
    @patch(
        "binance_common.websocket.aiohttp.ClientSession.ws_connect",
        new_callable=AsyncMock,
    )
    async def test_uses_the_supplied_token_without_fetching_one(
        self, mock_ws_connect, mock_send_request, mock_websocket
    ):
        mock_ws_connect.return_value = mock_websocket
        stream = WebSocketStreamBase(self._configuration(ws_token="supplied token"))

        await stream.create_connection()

        assert (
            mock_ws_connect.call_args[0][0]
            == "wss://test.com/ws/stream?token=supplied%20token"
        )
        mock_send_request.assert_not_called()
        assert stream._token_renewal_task is None

    @pytest.mark.asyncio
    @patch("binance_web3_common.websocket.send_request")
    @patch(
        "binance_common.websocket.aiohttp.ClientSession.ws_connect",
        new_callable=AsyncMock,
    )
    async def test_fetches_a_token_and_schedules_its_renewal(
        self, mock_ws_connect, mock_send_request, mock_websocket
    ):
        mock_ws_connect.return_value = mock_websocket
        mock_send_request.return_value = SimpleNamespace(
            data=lambda: {"data": {"token": "fetched-token"}}
        )
        stream = WebSocketStreamBase(
            self._configuration(api_key="test-api-key", api_secret="test-secret")
        )

        await stream.create_connection()

        assert (
            mock_ws_connect.call_args[0][0]
            == "wss://test.com/ws/stream?token=fetched-token"
        )
        assert (
            mock_send_request.call_args.kwargs["path"]
            == WEB3_WALLET_WS_STREAMS_TOKEN_ENDPOINT
        )
        assert mock_send_request.call_args.kwargs["is_signed"] is True
        assert stream._rest_configuration.base_path == WEB3_WALLET_REST_API_PROD_URL
        assert stream._token_renewal_task is not None

        stream._cancel_token_renewal()
        stream._close_rest_session()

    @pytest.mark.asyncio
    @patch(
        "binance_common.websocket.aiohttp.ClientSession.ws_connect",
        new_callable=AsyncMock,
    )
    async def test_the_token_survives_a_reconnect(
        self, mock_ws_connect, mock_websocket
    ):
        mock_ws_connect.return_value = mock_websocket
        stream = WebSocketStreamBase(self._configuration(ws_token="test-token"))

        await stream.create_connection()
        await stream.init_connection(
            stream.configuration.stream_url,
            stream.configuration,
            ws_id=stream.connections[0].id,
        )

        assert mock_ws_connect.await_count == 2
        assert [call[0][0] for call in mock_ws_connect.call_args_list] == [
            "wss://test.com/ws/stream?token=test-token"
        ] * 2

    @pytest.mark.asyncio
    async def test_requires_an_api_key_when_no_token_is_supplied(self):
        stream = WebSocketStreamBase(self._configuration())

        with pytest.raises(ValueError, match="'api_key' is required"):
            await stream.create_connection()

    @pytest.mark.asyncio
    @patch("binance_web3_common.websocket.send_request")
    async def test_raises_when_the_response_carries_no_token(self, mock_send_request):
        mock_send_request.return_value = SimpleNamespace(data=lambda: {"data": {}})
        stream = WebSocketStreamBase(self._configuration(api_key="test-api-key"))

        with pytest.raises(ValueError, match="did not include a token"):
            await stream.create_connection()

        stream._close_rest_session()

    @pytest.mark.asyncio
    async def test_renewal_refreshes_the_token_and_reconnects(self, mock_connection):
        stream = WebSocketStreamBase(self._configuration(api_key="test-api-key"))
        stream.connections = [mock_connection]
        stream._fetch_token = AsyncMock(return_value="renewed-token")
        stream.reconnect = AsyncMock()

        with patch(
            "binance_web3_common.websocket.asyncio.sleep", new_callable=AsyncMock
        ) as mock_sleep:
            mock_sleep.side_effect = [None, asyncio.CancelledError()]

            with pytest.raises(asyncio.CancelledError):
                await stream._renew_token_forever()

        mock_sleep.assert_any_await(WS_STREAMS_TOKEN_RENEWAL_SECONDS)
        assert stream._token == "renewed-token"
        stream.reconnect.assert_awaited_once_with(mock_connection, stream.configuration)

    @pytest.mark.asyncio
    async def test_renewal_skips_connections_that_are_closing(self, mock_connection):
        stream = WebSocketStreamBase(self._configuration(api_key="test-api-key"))
        mock_connection.close_initiated = True
        stream.connections = [mock_connection]
        stream.reconnect = AsyncMock()

        await stream._reconnect_with_new_token()

        stream.reconnect.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_renewal_survives_a_failed_attempt(self, mock_connection, caplog):
        stream = WebSocketStreamBase(self._configuration(api_key="test-api-key"))
        stream.connections = [mock_connection]
        stream._fetch_token = AsyncMock(
            side_effect=[RuntimeError("boom"), "renewed-token"]
        )
        stream.reconnect = AsyncMock()

        with caplog.at_level(logging.ERROR):
            with patch(
                "binance_web3_common.websocket.asyncio.sleep", new_callable=AsyncMock
            ) as mock_sleep:
                mock_sleep.side_effect = [None, None, asyncio.CancelledError()]

                with pytest.raises(asyncio.CancelledError):
                    await stream._renew_token_forever()

        assert "WebSocket auth token renewal failed: boom" in caplog.text
        assert stream._token == "renewed-token"
        stream.reconnect.assert_awaited_once_with(mock_connection, stream.configuration)

    @pytest.mark.asyncio
    async def test_closing_every_connection_stops_the_renewal(self):
        stream = WebSocketStreamBase(self._configuration(api_key="test-api-key"))
        stream._schedule_token_renewal()
        renewal_task = stream._token_renewal_task
        rest_session = MagicMock()
        stream._rest_session = rest_session

        with patch.object(
            WebSocketStreamsBaseCommon, "close_connection", new_callable=AsyncMock
        ) as mock_close:
            await stream.close_connection()

        await asyncio.sleep(0)

        assert stream._token_renewal_task is None
        assert renewal_task.cancelled()
        rest_session.close.assert_called_once()
        mock_close.assert_awaited_once_with(None, True)

    @pytest.mark.asyncio
    async def test_closing_a_single_connection_keeps_the_renewal(self, mock_connection):
        stream = WebSocketStreamBase(self._configuration(api_key="test-api-key"))
        stream._schedule_token_renewal()
        renewal_task = stream._token_renewal_task

        with patch.object(
            WebSocketStreamsBaseCommon, "close_connection", new_callable=AsyncMock
        ) as mock_close:
            await stream.close_connection(mock_connection, close_session=False)

        assert stream._token_renewal_task is renewal_task
        mock_close.assert_awaited_once_with(mock_connection, False)

        stream._cancel_token_renewal()
