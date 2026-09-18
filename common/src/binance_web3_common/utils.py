import json
import requests
import ssl
import time

from typing import Dict, List, Optional, Type, TypeVar

from pydantic import BaseModel

from binance_common.errors import (
    BadRequestError,
    ClientError,
    ForbiddenError,
    NetworkError,
    NotFoundError,
    RateLimitBanError,
    ServerError,
    TooManyRequestsError,
    UnauthorizedError,
)
from binance_common.utils import (
    CustomHTTPSAdapter,
    clean_none_value,
    encoded_string,
    get_iso_8601,
    get_random_int,
    get_signature,
    get_uuid,
    hmac_hashing,
    is_one_of_model,
    make_serializable,
    normalize_query_values,
    parse_proxies,
    parse_retry_after,
    redact_sensitive_info,
    should_retry_request,
    snake_to_camel,
    transform_query,
    web3_signature,
    ws_streams_placeholder,
)

from binance_common.models import ApiResponse
from binance_common.signature import Signers

from binance_web3_common.configuration import ConfigurationRestAPI

# The generic helpers, the response wrapper and the signers are inherited from
# `binance_common` and re-exported here to keep a single import site for the
# generated connector. Only `RateLimit`, `send_request` and
# `parse_rate_limit_headers`, which follow the Web3 Wallet signing scheme and its
# `x-oc-*` rate limit headers, are Web3 specific.
__all__ = [
    "ApiResponse",
    "CustomHTTPSAdapter",
    "RateLimit",
    "Signers",
    "clean_none_value",
    "encoded_string",
    "get_iso_8601",
    "get_random_int",
    "get_signature",
    "get_uuid",
    "hmac_hashing",
    "is_one_of_model",
    "make_serializable",
    "normalize_query_values",
    "parse_proxies",
    "parse_rate_limit_headers",
    "parse_retry_after",
    "redact_sensitive_info",
    "send_request",
    "should_retry_request",
    "snake_to_camel",
    "transform_query",
    "web3_signature",
    "ws_streams_placeholder",
]

T = TypeVar("T")


class RateLimit(BaseModel):
    """Represents the rate limit state reported by a response.

    Every field is optional: the API only sends the headers that apply to the
    endpoint that was called.

    :param limit: The maximum number of requests allowed in the window.
    :param remaining: How many requests are left in the current window.
    :param usedWeight: The request weight consumed so far.
    :param retryAfter: Retry time in seconds if rate-limited.
    """

    limit: Optional[int] = None
    remaining: Optional[int] = None
    usedWeight: Optional[int] = None
    retryAfter: Optional[int] = None


def send_request(
    session: requests.Session,
    configuration: ConfigurationRestAPI,
    method: str,
    path: str,
    payload: Optional[dict] = None,
    body: Optional[dict] = None,
    response_model: Optional[Type[T]] = None,
    is_signed: bool = False,
    signer: Optional[Signers] = None,
    web3_headers: Optional[dict] = None,
) -> ApiResponse[T]:
    """Sends an HTTP request with the specified configuration, method, path, and
    optional payload.

    The `send_request` function is responsible for sending an HTTP request with the provided parameters.
    It handles retries, error handling, and response processing. The function takes the following parameters:

    - `configuration`: The configuration object containing the necessary information for sending the request.
    - `method`: The HTTP method to use (e.g. "GET", "POST", etc.).
    - `path`: The API endpoint path.
    - `payload`: The request payload (optional).
    - `body`: The body data to send with the request (optional).
    - `response_model`: The response model to use for deserializing the response (optional).
    - `is_signed`: A boolean indicating whether the request should be signed (optional).
    - `signer`: The signer to use for signing the request (optional).
    - `web3_headers`: Specific headers for web3 requests

    The function returns the JSON response from the server, or raises an appropriate exception if an error occurs.
    """

    if payload is None:
        payload = {}

    headers = configuration.base_headers.copy()

    if configuration.compression:
        headers["Accept-Encoding"] = "gzip, deflate, br"

    url = f"{configuration.base_path}{path}"
    retries = configuration.retries if configuration else 0
    backoff = configuration.backoff / 1000 if configuration else 1
    timeout = configuration.timeout / 1000 if configuration else 10
    proxies = (
        parse_proxies(configuration.proxy)
        if configuration and configuration.proxy
        else None
    )

    if configuration.https_agent:
        if isinstance(configuration.https_agent, ssl.SSLContext):
            https_adapter = CustomHTTPSAdapter(configuration.https_agent)
        else:
            https_adapter = requests.adapters.HTTPAdapter()
        session.mount("https://", https_adapter)
        session.mount("http://", https_adapter)

    if not configuration.keep_alive:
        headers["Connection"] = "close"

    attempt = 0
    is_web3_request = web3_headers is not None

    if is_web3_request:
        timestamp = get_iso_8601()
        query_string = encoded_string(clean_none_value(payload))

        signature = (
            web3_signature(
                configuration,
                method,
                path,
                query_string,
                timestamp,
                body,
                signer,
            )
            if is_signed
            else ""
        )

        web3_headers = web3_headers or {}

        headers.update(
            {
                "X-OC-APIKEY": configuration.api_key,
                "X-OC-TIMESTAMP": timestamp,
                "X-OC-SIGN": signature,
                "X-OC-RECV-WINDOW": web3_headers.get("recv_window") or "15000",
                "X-OC-NONCE": web3_headers.get("nonce") or "",
            }
        )

    while attempt <= retries:
        try:
            response = session.request(
                method=method,
                url=url,
                params=encoded_string(clean_none_value(payload)),
                headers=headers,
                timeout=timeout,
                proxies=proxies,
                data=encoded_string(clean_none_value(body)) if body else None,
            )

            if response.status_code >= 400:
                status = response.status_code
                data = (
                    response.json()
                    if response.headers.get("Content-Type")
                    and response.headers.get("Content-Type").startswith(
                        "application/json"
                    )
                    else {}
                )

                if status == 400:
                    raise BadRequestError(
                        error_message=data.get("msg"), status_code=data.get("code")
                    )
                elif status == 401:
                    raise UnauthorizedError(
                        error_message=data.get("msg"), status_code=data.get("code")
                    )
                elif status == 403:
                    raise ForbiddenError(
                        error_message=data.get("msg"), status_code=data.get("code")
                    )
                elif status == 404:
                    raise NotFoundError(
                        error_message=data.get("msg"), status_code=data.get("code")
                    )
                elif status == 418:
                    raise RateLimitBanError(
                        error_message=data.get("msg"),
                        status_code=data.get("code"),
                        retry_after=parse_retry_after(response.headers),
                    )
                elif status == 429:
                    raise TooManyRequestsError(
                        error_message=data.get("msg"),
                        status_code=data.get("code"),
                        retry_after=parse_retry_after(response.headers),
                    )
                elif 500 <= status < 600:
                    raise ServerError(
                        error_message=f"Server error: {status}", status_code=status
                    )
                else:
                    raise ClientError(error_message=data.get("msg"))

            parsed = json.loads(response.text)
            is_list = isinstance(parsed, list)
            is_oneof = is_one_of_model(response_model)
            is_flat_list = is_list and (
                len(parsed) == 0
                or (not isinstance(parsed[0], list) if is_list else False)
            )

            if (is_list and not is_flat_list) or not response_model:
                def data_function():
                    return parsed
            elif is_oneof or is_list or hasattr(response_model, "from_dict"):
                def data_function():
                    return response_model.from_dict(parsed)
            else:
                def data_function():
                    return response_model.model_validate(parsed)
            try:
                data_function()
                final_data_function = data_function
            except Exception:
                def final_data_function():
                    return parsed

            return ApiResponse[T](
                data_function=final_data_function,
                status=response.status_code,
                headers=response.headers,
                rate_limits=parse_rate_limit_headers(response.headers),
            )
        except requests.RequestException as e:
            attempt += 1

            if should_retry_request(e, method, retries - attempt):
                time.sleep(backoff * attempt)
            else:
                raise NetworkError(error_message=f"Network error: {str(e)}") from e

    raise Exception(f"Request failed after {retries} retries.")


def parse_rate_limit_headers(headers: Dict[str, str]) -> List[RateLimit]:
    """Parses the `X-OC-*` rate limit headers from the response headers.

    Args:
        headers (Dict[str, str]): The response headers.

    Returns:
        List[RateLimit]: A single-element list describing the current rate limit
            state, or an empty list when the response carried none of the headers.
    """

    normalized = {
        key.lower(): value for key, value in headers.items() if value is not None
    }

    def header_int(name: str) -> Optional[int]:
        """Reads a header as an integer.

        Args:
            name (str): The lowercase header name.

        Returns:
            Optional[int]: The parsed value, or `None` when the header is absent
                or is not an integer.
        """

        value = normalized.get(name)

        if isinstance(value, (list, tuple)):
            value = value[0] if value else None

        try:
            return int(str(value))
        except (TypeError, ValueError):
            return None

    fields = {
        "limit": header_int("x-oc-ratelimit-limit"),
        "remaining": header_int("x-oc-ratelimit-remaining"),
        "usedWeight": header_int("x-oc-used-weight"),
        "retryAfter": parse_retry_after(headers),
    }
    fields = {name: value for name, value in fields.items() if value is not None}

    return [RateLimit(**fields)] if fields else []
