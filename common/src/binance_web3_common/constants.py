from binance_common.constants import (
    DEFAULT_RECONNECT_ATTEMPTS,
    MAX_RECONNECT_ATTEMPTS,
    WebsocketMode,
)

# The connection settings are inherited from `binance_common` and re-exported
# here to keep a single import site for the generated connector.
__all__ = [
    "DEFAULT_RECONNECT_ATTEMPTS",
    "MAX_RECONNECT_ATTEMPTS",
    "WebsocketMode",
    "WS_STREAMS_TOKEN_RENEWAL_SECONDS",
    "WEB3_WALLET_REST_API_PROD_URL",
    "WEB3_WALLET_WS_STREAMS_PROD_URL",
    "WEB3_WALLET_WS_STREAMS_TOKEN_ENDPOINT",
]

# Auth tokens are valid for 7 days. They are renewed at 6 days to keep a
# 24-hour safety margin.
WS_STREAMS_TOKEN_RENEWAL_SECONDS = 6 * 24 * 3600

# Web3 Wallet constants
WEB3_WALLET_REST_API_PROD_URL = "https://web3.binance.com/build"
WEB3_WALLET_WS_STREAMS_PROD_URL = "wss://web3-stream.binance.com/w3w"
WEB3_WALLET_WS_STREAMS_TOKEN_ENDPOINT = "/api/v1/dex/market/wss/auth/token"
