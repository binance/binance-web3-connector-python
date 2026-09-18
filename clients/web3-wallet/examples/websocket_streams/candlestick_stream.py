import asyncio
import os
import logging

from binance_sdk_web3_wallet.web3_wallet import (
    Web3Wallet,
    WEB3_WALLET_WS_STREAMS_PROD_URL,
    ConfigurationWebSocketStreams,
)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create configuration for the WebSocket Streams
configuration_ws_streams = ConfigurationWebSocketStreams(
    api_key=os.getenv("API_KEY", ""),
    api_secret=os.getenv("API_SECRET", ""),
    stream_url=os.getenv("STREAM_URL", WEB3_WALLET_WS_STREAMS_PROD_URL),
)

# Initialize Web3Wallet client
client = Web3Wallet(config_ws_streams=configuration_ws_streams)


async def candlestick_stream():
    connection = None
    try:
        connection = await client.websocket_streams.create_connection()

        stream = await connection.candlestick_stream(
            bar="1s",
            chain_id="CT_501",
            contract_address="C3DwDjT17gDvvCYC2nsdGHxDHVmQRdhKfpAdqQ29pump",
        )
        stream.on("message", lambda data: print(f"{data}"))

        await asyncio.sleep(5)
        await stream.unsubscribe()
    except Exception as e:
        logging.error(f"candlestick_stream() error: {e}")
    finally:
        if connection:
            await connection.close_connection(close_session=True)


if __name__ == "__main__":
    asyncio.run(candlestick_stream())
