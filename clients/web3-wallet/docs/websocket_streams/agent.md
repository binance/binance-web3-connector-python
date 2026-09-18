# Agent

```python
import asyncio
import ssl
import logging

from binance_web3_common.configuration import ConfigurationWebSocketStreams
from binance_sdk_web3_wallet.web3_wallet import Web3Wallet

logging.basicConfig(level=logging.INFO)

configuration_ws_streams = ConfigurationWebSocketStreams(
    api_key="api-key",
    api_secret="api-secret",
    https_agent=ssl.create_default_context(),
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
