# Binance Python Web3 Wallet

[![Build Status](https://img.shields.io/github/actions/workflow/status/binance/binance-web3-connector-python/ci.yaml)](https://github.com/binance/binance-web3-connector-python/actions)
[![Open Issues](https://img.shields.io/github/issues/binance/binance-web3-connector-python)](https://github.com/binance/binance-web3-connector-python/issues)
[![Code Style: Black](https://img.shields.io/badge/code_style-black-black)](https://black.readthedocs.io/en/stable/)
[![PyPI version](https://img.shields.io/pypi/v/binance-web3-wallet)](https://pypi.python.org/pypi/binance-web3-wallet)
[![PyPI Downloads](https://img.shields.io/pypi/dm/binance-web3-wallet.svg)](https://pypi.org/project/binance-web3-wallet/)
[![Python version](https://img.shields.io/pypi/pyversions/binance-web3-wallet)](https://www.python.org/downloads/)
[![Known Vulnerabilities](https://img.shields.io/badge/security-scanned-brightgreen)](https://github.com/binance/binance-web3-connector-python/security)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is a client library for the Binance Web3 Wallet API, enabling developers to interact programmatically with Binance's Web3 Wallet platform. The library provides tools to programmatically leverage Binance in-house algorithmic trading capability to automate order execution strategy, improve execution transparency and give users smart access to the available market liquidity through the REST API:

- [REST API](./src/binance_sdk_web3_wallet/rest_api/rest_api.py)

## Table of Contents

- [Supported Features](#supported-features)
- [Installation](#installation)
- [Documentation](#documentation)
- [REST APIs](#rest-apis)
- [Websocket Streams](#websocket-streams)
- [Testing](#testing)
- [Contributing](#contributing)
- [Licence](#licence)

## Supported Features

- REST API Endpoints
- Inclusion of test cases and examples for quick onboarding.

## Installation

To use this library, ensure your environment is running Python version **3.10** or later.

```bash
pip install binance-web3-wallet
```

## Documentation

For detailed information, refer to the [Binance API Documentation](https://web3.binance.com/en/dev-docs).

### REST APIs

All REST API endpoints are available through the [`rest_api`](./src/binance_sdk_web3_wallet/rest_api/rest_api.py) module. Note that some endpoints require authentication using your Binance API credentials.

```python
from binance_sdk_web3_wallet.web3_wallet import (
    Web3Wallet,
    ConfigurationRestAPI,
    WEB3_WALLET_REST_API_PROD_URL,
)

logging.basicConfig(level=logging.INFO)
configuration = ConfigurationRestAPI(api_key="your-api-key", api_secret="your-api-secret", base_path=WEB3_WALLET_REST_API_PROD_URL)

client = Web3Wallet(config_rest_api=configuration_rest_api)

try:
    response = client.rest_api.get_price_info()

    rate_limits = response.rate_limits
    logging.info(f"get_price_info() rate limits: {rate_limits}")

    data = response.data()
    logging.info(f"get_price_info() response: {data}")
except Exception as e:
    logging.error(f"exchange_info() error: {e}")
```

More examples can be found in the [`examples/rest_api`](./examples/rest_api/) folder.

#### Configuration Options

The REST API supports the following advanced configuration options:

- `timeout`: Timeout for requests in milliseconds (default: 1000 ms).
- `proxy`: Proxy configuration:
  - `host`: Proxy server hostname.
  - `port`: Proxy server port.
  - `protocol`: Proxy protocol (http or https).
  - `auth`: Proxy authentication credentials:
    - `username`: Proxy username.
    - `password`: Proxy password.
- `keep_alive`: Enable HTTP keep-alive (default: true).
- `compression`: Enable response compression (default: true).
- `retries`: Number of retry attempts for failed requests (default: 3).
- `backoff`: Delay in milliseconds between retries (default: 1000 ms).
- `https_agent`: Custom HTTPS agent for advanced TLS configuration.
- `private_key`: RSA or ED25519 private key for authentication.
- `private_key_passphrase`: Passphrase for the private key, if encrypted.

##### Timeout

You can configure a timeout for requests in milliseconds. If the request exceeds the specified timeout, it will be aborted. See the [Timeout example](./docs/rest_api/timeout.md) for detailed usage.

##### Proxy

The REST API supports HTTP/HTTPS proxy configurations. See the [Proxy example](./docs/rest_api/proxy.md) for detailed usage.

##### Keep-Alive

Enable HTTP keep-alive for persistent connections. See the [Keep-Alive example](./docs/rest_api/keepAlive.md) for detailed usage.

##### Compression

Enable or disable response compression. See the [Compression example](./docs/rest_api/compression.md) for detailed usage.

##### Retries

Configure the number of retry attempts and delay in milliseconds between retries for failed requests. See the [Retries example](./docs/rest_api/retries.md) for detailed usage.

##### HTTPS Agent

Customize the HTTPS agent for advanced TLS configurations. See the [HTTPS Agent example](./docs/rest_api/httpsAgent.md) for detailed usage.

##### Key Pair Based Authentication

The REST API supports key pair-based authentication for secure communication. You can use `RSA` or `ED25519` keys for signing requests. See the [Key Pair Based Authentication example](./docs/rest_api/key-pair-authentication.md) for detailed usage.

##### Certificate Pinning

To enhance security, you can use certificate pinning with the `https_agent` option in the configuration. This ensures the client only communicates with servers using specific certificates. See the [Certificate Pinning example](./docs/rest_api/certificate-pinning.md) for detailed usage.

#### Error Handling

The REST API provides detailed error types to help you handle issues effectively:

- `ClientError`: Represents an error that occurred in the SDK client.
- `RequiredError`: Thrown when a required parameter is missing or undefined.
- `UnauthorizedError`: Indicates missing or invalid authentication credentials.
- `ForbiddenError`: Access to the requested resource is forbidden.
- `TooManyRequestsError`: Rate limit exceeded.
- `RateLimitBanError`: IP address banned for exceeding rate limits.
- `ServerError`: Internal server error, optionally includes a status code.
- `NetworkError`: Issues with network connectivity.
- `NotFoundError`: Resource not found.
- `BadRequestError`: Invalid request or one that cannot be served.

See the [Error Handling example](./docs/rest_api/error-handling.md) for detailed usage.

If basePath is not provided, it defaults to https://web3.binance.com/build.

### Websocket Streams

WebSocket Streams provide real-time data feeds for market trades, candlesticks, and more. Use the [websocket-streams](./src/binance_sdk_spot/websocket_streams/websocket_streams.py) module to subscribe to these streams.

```python
import asyncio
import logging

from binance_web3_common.configuration import ConfigurationWebSocketStreams
from binance_sdk_web3_wallet.web3_wallet import Web3Wallet

logging.basicConfig(level=logging.INFO)

configuration_ws_streams = ConfigurationWebSocketStreams(
    api_key="api-key",
    api_secret="api-secret",
)

client = Web3Wallet(config_ws_streams=configuration_ws_streams)


async def price_stream():
    connection = None
    try:
        connection = await client.websocket_streams.create_connection()

        stream = await connection.price_stream(
            chain_id="CT_501",
            contract_address="C3DwDjT17gDvvCYC2nsdGHxDHVmQRdhKfpAdqQ29pump",
        )
        stream.on("message", lambda data: print(f"{data}"))
    except Exception as e:
        logging.error(f"price_stream() error: {e}")

if __name__ == "__main__":
    asyncio.run(price_stream())
```

More examples are available in the [`examples/websocket-streams`](./examples/websocket_streams/) folder.

#### Configuration Options

The WebSocket Streams API supports the following advanced configuration options:

- `reconnect_delay`: Delay (ms) between reconnections.
- `compression`: Enable response compression.
- `mode`: Choose between `single` and `pool` connection modes.
  - `single`: A single WebSocket connection.
  - `pool`: A pool of WebSocket connections.
- `pool_size`: Define the number of WebSocket connections in pool mode.
- `https_agent`: Custom HTTPS agent for advanced TLS configuration.
- `user_agent`: Custom user agent string for WebSocket Streams.
- `wsTokenEndpoint`: Endpoint to retrieve a WebSocket token for authentication (default: /api/v1/dex/market/wss/auth/token).
- `wsToken`: Provide a WebSocket token for authentication if needed (default: token retrieved from `wsTokenEndpoint` automatically).

##### Reconnect Delay

Specify the delay in milliseconds between WebSocket reconnection attempts for streams. See the [Reconnect Delay example](./docs/websocket_streams/reconnect-delay.md) for detailed usage.

##### Compression

Enable or disable compression for WebSocket Streams messages. See the [Compression example](./docs/websocket_streams/compression.md) for detailed usage.

##### Connection Mode

Choose between `single` and `pool` connection modes for WebSocket Streams. The `single` mode uses a single WebSocket connection, while the `pool` mode uses a pool of WebSocket connections. See the [Connection Mode example](./docs/websocket_streams/connection-mode.md) for detailed usage.

##### WebSocket Http Agent

Customize the agent for advanced configurations. See the [WebSocket Http Agent example](./docs/websocket_streams/agent.md) for detailed usage.

#### Unsubscribing from Streams

You can unsubscribe from specific WebSocket streams using the `unsubscribe` method. This is useful for managing active subscriptions without closing the connection.

```python
import asyncio
import logging

from binance_web3_common.configuration import ConfigurationWebSocketStreams
from binance_sdk_web3_wallet.web3_wallet import Web3Wallet

logging.basicConfig(level=logging.INFO)

configuration_ws_streams = ConfigurationWebSocketStreams(
    api_key="api-key",
    api_secret="api-secret",
)

client = Web3Wallet(config_ws_streams=configuration_ws_streams)


async def price_stream():
    connection = None
    try:
        connection = await client.websocket_streams.create_connection()

        stream = await connection.price_stream(
            chain_id="CT_501",
            contract_address="C3DwDjT17gDvvCYC2nsdGHxDHVmQRdhKfpAdqQ29pump",
        )
        stream.on("message", lambda data: print(f"{data}"))

        await asyncio.sleep(5)
        await stream.unsubscribe()
    except Exception as e:
        logging.error(f"price_stream() error: {e}")
    finally:
        if connection:
            await connection.close_connection(close_session=True)


if __name__ == "__main__":
    asyncio.run(price_stream())
```

If `wsURL` is not provided, it defaults to `wss://web3-stream.binance.com/w3w`.

### Automatic Connection Renewal

The WebSocket connection is automatically renewed for both WebSocket API and WebSocket Streams connections, before the 24 hours expiration of the API key. This ensures continuous connectivity.

## Testing

To run the tests, ensure you have [Poetry](https://python-poetry.org/) installed, then execute the following commands:

```bash
poetry install
poetry run pytest ./tests
```

The tests cover:

- REST API endpoints
- Error handling and edge cases

## Contributing

Contributions are welcome!

Since this repository contains auto-generated code, we encourage you to start by opening a GitHub issue to discuss your ideas or suggest improvements. This helps ensure that changes align with the project's goals and auto-generation processes.

To contribute:

1. Open a GitHub issue describing your suggestion or the bug you've identified.
2. If it's determined that changes are necessary, the maintainers will merge the changes into the main branch.

Please ensure that all tests pass if you're making a direct contribution. Submit a pull request only after discussing and confirming the change.

Thank you for your contributions!

## Licence

This project is licensed under the MIT License. See the [LICENCE](./LICENCE) file for details.
