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


def calculate_lp_add_paired_amounts():
    try:
        response = client.rest_api.calculate_lp_add_paired_amounts(
            address="address_example",
            investment_id="investment_id_example",
            input_token=(),
        )

        rate_limits = response.rate_limits
        logging.info(f"calculate_lp_add_paired_amounts() rate limits: {rate_limits}")

        data = response.data()
        logging.info(f"calculate_lp_add_paired_amounts() response: {data}")
    except Exception as e:
        logging.error(f"calculate_lp_add_paired_amounts() error: {e}")


if __name__ == "__main__":
    calculate_lp_add_paired_amounts()
