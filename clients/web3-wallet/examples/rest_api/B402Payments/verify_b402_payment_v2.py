import os
import logging

from binance_sdk_web3_wallet.web3_wallet import (
    Web3Wallet,
    ConfigurationRestAPI,
    WEB3_WALLET_REST_API_PROD_URL,
)


# Configure logging
logging.basicConfig(level=logging.INFO)

# Create configuration for the REST API
configuration_rest_api = ConfigurationRestAPI(
    api_key=os.getenv("API_KEY", ""),
    api_secret=os.getenv("API_SECRET", ""),
    base_path=os.getenv("BASE_PATH", WEB3_WALLET_REST_API_PROD_URL),
)

# Initialize Web3Wallet client
client = Web3Wallet(config_rest_api=configuration_rest_api)


def verify_b402_payment_v2():
    try:
        response = client.rest_api.verify_b402_payment_v2(
            body=(),
        )

        rate_limits = response.rate_limits
        logging.info(f"verify_b402_payment_v2() rate limits: {rate_limits}")

        data = response.data()
        logging.info(f"verify_b402_payment_v2() response: {data}")
    except Exception as e:
        logging.error(f"verify_b402_payment_v2() error: {e}")


if __name__ == "__main__":
    verify_b402_payment_v2()
