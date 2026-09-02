import os
import logging

from binance_sdk_web3_wallet.web3_wallet import (
    Web3Wallet,
    ConfigurationRestAPI,
    WEB3_WALLET_REST_API_PROD_URL,
)
from binance_sdk_web3_wallet.rest_api.models import ListDeFiInvestmentsInvestTypeEnum


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


def list_de_fi_investments():
    try:
        response = client.rest_api.list_de_fi_investments(
            invest_type=ListDeFiInvestmentsInvestTypeEnum["invest_type_example"].value,
        )

        rate_limits = response.rate_limits
        logging.info(f"list_de_fi_investments() rate limits: {rate_limits}")

        data = response.data()
        logging.info(f"list_de_fi_investments() response: {data}")
    except Exception as e:
        logging.error(f"list_de_fi_investments() error: {e}")


if __name__ == "__main__":
    list_de_fi_investments()
