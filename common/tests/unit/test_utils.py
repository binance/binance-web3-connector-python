import importlib
import json
import requests
import unittest

from typing import List
from unittest.mock import Mock, patch

from binance_common.errors import (
    BadRequestError,
    UnauthorizedError,
    ForbiddenError,
    NotFoundError,
    RateLimitBanError,
    TooManyRequestsError,
    ServerError,
    NetworkError,
)
from binance_web3_common.configuration import ConfigurationRestAPI
from binance_web3_common.utils import (
    RateLimit,
    parse_rate_limit_headers,
    send_request,
)


# The generic helpers, the configuration, the response wrapper and the signers are
# inherited from `binance_common` and tested there. These tests only cover what
# `binance_web3_common` adds: the Web3 signing scheme, its authentication headers
# and the `x-oc-*` rate limit headers.


class TestReExportedHelpers(unittest.TestCase):
    def test_every_exported_name_resolves(self):
        module = importlib.import_module("binance_web3_common.utils")

        for name in module.__all__:
            with self.subTest(name=name):
                self.assertTrue(hasattr(module, name))


class TestSendRequest(unittest.TestCase):
    def setUp(self):
        self.session = Mock(spec=requests.Session)
        self.configuration = ConfigurationRestAPI(
            api_key="test_key",
            api_secret="test_secret",
            base_path="https://api.test.com",
            retries=3,
            backoff=1,
            timeout=5000,
            proxy=None,
            compression=False,
            https_agent=None,
            keep_alive=False,
        )
        self.method = "GET"
        self.path = "/test"
        self.url = f"{self.configuration.base_path}{self.path}"

    def test_base_headers_carry_the_web3_authentication(self):
        """The Web3 Wallet API expects the API key in `X-OC-APIKEY`."""
        self.assertEqual(
            self.configuration.base_headers,
            {"Content-Type": "application/json", "X-OC-APIKEY": "test_key"},
        )
        self.assertEqual(ConfigurationRestAPI().base_headers["X-OC-APIKEY"], "")
        self.assertEqual(
            ConfigurationRestAPI(custom_headers={"X-Custom": "value"}).base_headers[
                "X-Custom"
            ],
            "value",
        )

    @patch("binance_web3_common.utils.encoded_string", side_effect=lambda x: x)
    @patch("binance_web3_common.utils.clean_none_value", side_effect=lambda x: x)
    @patch("binance_web3_common.utils.parse_rate_limit_headers", return_value=[])
    def test_successful_request(
        self, mock_parse_rate_limits, mock_clean_none, mock_encoded_string
    ):
        """Test successful request (200 response)."""
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = {"success": True}
        mock_response.text = json.dumps({"success": True})

        self.session.request.return_value = mock_response

        response = send_request(
            self.session, self.configuration, self.method, self.path, {"param": "value"}
        )

        self.assertEqual(response.data(), {"success": True})
        self.assertEqual(response.status, 200)
        self.assertEqual(response.headers, mock_response.headers)
        self.assertEqual(response.rate_limits, [])

        headers = self.configuration.base_headers
        headers["Connection"] = "close"

        self.session.request.assert_called_once_with(
            method=self.method,
            url=self.url,
            params={"param": "value"},
            headers=headers,
            timeout=5,
            proxies=None,
            data=None,
        )

    @patch("binance_web3_common.utils.encoded_string", side_effect=lambda x: x)
    @patch("binance_web3_common.utils.clean_none_value", side_effect=lambda x: x)
    @patch("binance_web3_common.utils.parse_rate_limit_headers", return_value=[])
    def test_successful_request_empty_array_response(
        self, mock_parse_rate_limits, mock_clean_none, mock_encoded_string
    ):
        """Test successful request (200 response)."""
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = []
        mock_response.text = json.dumps([])

        self.session.request.return_value = mock_response

        response = send_request(
            self.session, self.configuration, self.method, self.path, {"param": "value"}
        )

        self.assertEqual(response.data(), [])
        self.assertEqual(response.status, 200)
        self.assertEqual(response.headers, mock_response.headers)
        self.assertEqual(response.rate_limits, [])

        headers = self.configuration.base_headers
        headers["Connection"] = "close"

        self.session.request.assert_called_once_with(
            method=self.method,
            url=self.url,
            params={"param": "value"},
            headers=headers,
            timeout=5,
            proxies=None,
            data=None,
        )

    @patch("binance_web3_common.utils.encoded_string", side_effect=lambda x: x)
    @patch("binance_web3_common.utils.clean_none_value", side_effect=lambda x: x)
    def test_client_errors(self, mock_clean_none, mock_encoded_string):
        """Test 400-499 errors raising appropriate exceptions."""
        error_cases = {
            400: BadRequestError,
            401: UnauthorizedError,
            403: ForbiddenError,
            404: NotFoundError,
            418: RateLimitBanError,
            429: TooManyRequestsError,
        }

        for status, exception in error_cases.items():
            with self.subTest(status=status):
                mock_response = Mock(
                    status_code=status, headers={"Content-Type": "application/json"}
                )

                mock_response.json.return_value = {
                    "msg": f"Error {status}",
                    "code": 10001,
                }
                self.session.request.return_value = mock_response

                with self.assertRaises(exception) as context:
                    send_request(
                        self.session, self.configuration, self.method, self.path, {}
                    )

                self.assertEqual(context.exception.error_message, f"Error {status}")
                self.assertEqual(context.exception.status_code, 10001)

                mock_response.json.return_value = {}
                self.session.request.return_value = mock_response

                with self.assertRaises(exception) as context:
                    send_request(
                        self.session, self.configuration, self.method, self.path, {}
                    )

                self.assertEqual(
                    context.exception.error_message, exception().error_message
                )
                self.assertIsNone(getattr(context.exception, "status_code", None))

    @patch("binance_web3_common.utils.encoded_string", side_effect=lambda x: x)
    @patch("binance_web3_common.utils.clean_none_value", side_effect=lambda x: x)
    def test_rate_limit_errors_expose_retry_after(
        self, mock_clean_none, mock_encoded_string
    ):
        cases = {418: RateLimitBanError, 429: TooManyRequestsError}

        for status, exception in cases.items():
            for header, expected in (
                ({"Retry-After": "30"}, 30),
                ({"retry-after": "30"}, 30),
                ({}, None),
                ({"Retry-After": "Wed, 21 Oct 2015 07:28:00 GMT"}, None),
            ):
                with self.subTest(status=status, header=header):
                    mock_response = Mock(
                        status_code=status,
                        headers={"Content-Type": "application/json", **header},
                    )
                    mock_response.json.return_value = {"msg": "Too many requests"}
                    self.session.request.return_value = mock_response

                    with self.assertRaises(exception) as context:
                        send_request(
                            self.session, self.configuration, self.method, self.path, {}
                        )

                    self.assertEqual(context.exception.retry_after, expected)

    @patch("binance_web3_common.utils.encoded_string", side_effect=lambda x: x)
    @patch("binance_web3_common.utils.clean_none_value", side_effect=lambda x: x)
    def test_server_errors(self, mock_clean_none, mock_encoded_string):
        """Test 500-599 server errors raising ServerError."""
        for status in [500, 502, 503, 504]:
            with self.subTest(status=status):
                mock_response = Mock(status_code=status)
                mock_response.json.return_value = {"msg": "Server Error"}
                self.session.request.return_value = mock_response

                with self.assertRaises(ServerError) as context:
                    send_request(
                        self.session, self.configuration, self.method, self.path, {}
                    )

                self.assertEqual(str(context.exception), f"Server error: {status}")

    @patch("binance_web3_common.utils.encoded_string", side_effect=lambda x: x)
    @patch("binance_web3_common.utils.clean_none_value", side_effect=lambda x: x)
    @patch(
        "binance_web3_common.utils.should_retry_request",
        side_effect=lambda e, m, r: r > 0
        and (getattr(e, "response", None) is None or e.response.status_code != 500),
    )
    @patch("time.sleep", return_value=None)
    def test_network_error_with_retry(
        self, mock_sleep, mock_should_retry, mock_clean_none, mock_encoded_string
    ):
        """Test request retrying on network errors."""

        mock_response = Mock(status_code=500)
        self.session.request.side_effect = [
            requests.RequestException("Network Error"),
            mock_response,
        ]

        with self.assertRaises(ServerError):
            send_request(self.session, self.configuration, self.method, self.path, {})

    @patch("binance_web3_common.utils.encoded_string", side_effect=lambda x: x)
    @patch("binance_web3_common.utils.clean_none_value", side_effect=lambda x: x)
    @patch("binance_web3_common.utils.should_retry_request", return_value=False)
    def test_network_error_no_retry(
        self, mock_should_retry, mock_clean_none, mock_encoded_string
    ):
        """Test request failure when retry is not allowed."""
        self.session.request.side_effect = requests.RequestException("Network Error")

        with self.assertRaises(NetworkError) as context:
            send_request(self.session, self.configuration, self.method, self.path, {})

        self.assertEqual(str(context.exception), "Network error: Network Error")
        self.assertEqual(mock_should_retry.call_count, 1)

    @patch("binance_web3_common.utils.encoded_string", side_effect=lambda x: x)
    @patch("binance_web3_common.utils.clean_none_value", side_effect=lambda x: x)
    def test_correct_headers_and_proxies(self, mock_clean_none, mock_encoded_string):
        """Ensure correct headers and proxies are used in request."""
        self.configuration.proxy = {
            "protocol": "https",
            "host": "127.0.0.1",
            "port": 8080,
        }
        self.configuration.compression = True

        mock_response = Mock(status_code=200)
        mock_response.json.return_value = {"success": True}
        mock_response.headers = {"x-mbx-used-weight-1m": "10"}
        mock_response.text = json.dumps({"success": True})
        self.session.request.return_value = mock_response

        send_request(self.session, self.configuration, self.method, self.path, {})

        self.session.request.assert_called_once()
        _, kwargs = self.session.request.call_args

        self.assertEqual(kwargs["headers"]["Accept-Encoding"], "gzip, deflate, br")
        self.assertEqual(
            kwargs["proxies"],
            {"http": "https://127.0.0.1:8080", "https": "https://127.0.0.1:8080"},
        )

    @patch("binance_web3_common.utils.encoded_string", side_effect=lambda x: x)
    @patch("binance_web3_common.utils.clean_none_value", side_effect=lambda x: x)
    @patch("binance_web3_common.utils.should_retry_request", return_value=False)
    def test_request_fails_after_retries(
        self, mock_should_retry, mock_clean_none, mock_encoded_string
    ):
        """Ensure request fails after max retries are exhausted."""
        self.configuration.retries = 2
        self.session.request.side_effect = requests.RequestException("Final Failure")

        with self.assertRaises(NetworkError) as context:
            send_request(self.session, self.configuration, self.method, self.path, {})

        self.assertEqual(str(context.exception), "Network error: Final Failure")


    @patch("binance_web3_common.utils.get_iso_8601", return_value="2026-06-03T10:20:30.123Z")
    @patch("binance_web3_common.utils.web3_signature", return_value="web3_signed_signature")
    @patch("binance_web3_common.utils.clean_none_value", side_effect=lambda x: x)
    @patch("binance_web3_common.utils.encoded_string", return_value="param=value")
    @patch("binance_web3_common.utils.parse_rate_limit_headers", return_value=[])
    def test_web3_signed_request_adds_web3_headers(
        self,
        mock_parse_rate_limits,
        mock_encoded_string,
        mock_clean_none,
        mock_web3_signature,
        mock_get_iso_8601,
    ):
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = {"success": True}
        mock_response.text = json.dumps({"success": True})
        mock_response.headers = {}

        self.session.request.return_value = mock_response

        response = send_request(
            self.session,
            self.configuration,
            "POST",
            self.path,
            payload={"param": "value"},
            body={"field": "data"},
            is_signed=True,
            web3_headers={"recv_window": "20000", "nonce": "abc123"},
        )

        self.assertEqual(response.data(), {"success": True})
        self.session.request.assert_called_once()

        _, kwargs = self.session.request.call_args
        headers = kwargs["headers"]

        self.assertEqual(kwargs["params"], "param=value")
        self.assertEqual(kwargs["data"], "param=value")
        self.assertEqual(headers["X-OC-APIKEY"], self.configuration.api_key)
        self.assertEqual(headers["X-OC-TIMESTAMP"], "2026-06-03T10:20:30.123Z")
        self.assertEqual(headers["X-OC-SIGN"], "web3_signed_signature")
        self.assertEqual(headers["X-OC-RECV-WINDOW"], "20000")
        self.assertEqual(headers["X-OC-NONCE"], "abc123")

        mock_web3_signature.assert_called_once_with(
            self.configuration,
            "POST",
            self.path,
            "param=value",
            "2026-06-03T10:20:30.123Z",
            {"field": "data"},
            None,
        )

    @patch("binance_web3_common.utils.get_iso_8601", return_value="2026-06-03T10:20:30.123Z")
    @patch("binance_web3_common.utils.web3_signature", return_value="web3_signed_signature")
    @patch("binance_web3_common.utils.clean_none_value", side_effect=lambda x: x)
    @patch("binance_web3_common.utils.encoded_string", return_value="param=value")
    @patch("binance_web3_common.utils.parse_rate_limit_headers", return_value=[])
    def test_web3_signed_request_uses_default_recv_window_and_nonce(
        self,
        mock_parse_rate_limits,
        mock_encoded_string,
        mock_clean_none,
        mock_web3_signature,
        mock_get_iso_8601,
    ):
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = {"success": True}
        mock_response.text = json.dumps({"success": True})
        mock_response.headers = {}

        self.session.request.return_value = mock_response

        response = send_request(
            self.session,
            self.configuration,
            "GET",
            self.path,
            payload={"param": "value"},
            is_signed=True,
            web3_headers={},
        )

        self.assertEqual(response.data(), {"success": True})

        _, kwargs = self.session.request.call_args
        headers = kwargs["headers"]

        self.assertEqual(headers["X-OC-RECV-WINDOW"], "15000")
        self.assertEqual(headers["X-OC-NONCE"], "")
        self.assertEqual(headers["X-OC-SIGN"], "web3_signed_signature")

    @patch("binance_web3_common.utils.get_iso_8601", return_value="2026-06-03T10:20:30.123Z")
    @patch("binance_web3_common.utils.web3_signature")
    @patch("binance_web3_common.utils.clean_none_value", side_effect=lambda x: x)
    @patch("binance_web3_common.utils.encoded_string", return_value="param=value")
    @patch("binance_web3_common.utils.parse_rate_limit_headers", return_value=[])
    def test_web3_unsigned_request_does_not_sign(
        self,
        mock_parse_rate_limits,
        mock_encoded_string,
        mock_clean_none,
        mock_web3_signature,
        mock_get_iso_8601,
    ):
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = {"success": True}
        mock_response.text = json.dumps({"success": True})
        mock_response.headers = {}

        self.session.request.return_value = mock_response

        response = send_request(
            self.session,
            self.configuration,
            "GET",
            self.path,
            payload={"param": "value"},
            is_signed=False,
            web3_headers={},
        )

        self.assertEqual(response.data(), {"success": True})

        _, kwargs = self.session.request.call_args
        headers = kwargs["headers"]

        self.assertEqual(headers["X-OC-SIGN"], "")
        mock_web3_signature.assert_not_called()


class TestParseRateLimitHeaders(unittest.TestCase):
    def test_parse_all_headers(self):
        """Test parsing every supported rate limit header"""
        headers = {
            "x-oc-ratelimit-limit": "1200",
            "x-oc-ratelimit-remaining": "1150",
            "x-oc-used-weight": "50",
            "retry-after": "10",
        }

        expected_output: List[RateLimit] = [
            RateLimit(limit=1200, remaining=1150, usedWeight=50, retryAfter=10)
        ]

        self.assertEqual(parse_rate_limit_headers(headers), expected_output)

    def test_parse_partial_headers(self):
        """Test parsing a response that only carries some of the headers"""
        headers = {"x-oc-used-weight": "50"}

        expected_output: List[RateLimit] = [RateLimit(usedWeight=50)]

        self.assertEqual(parse_rate_limit_headers(headers), expected_output)

    def test_parse_mixed_case_headers(self):
        """Test that header names are matched case-insensitively"""
        headers = {"X-OC-RateLimit-Limit": "1200", "X-OC-Used-Weight": "50"}

        expected_output: List[RateLimit] = [RateLimit(limit=1200, usedWeight=50)]

        self.assertEqual(parse_rate_limit_headers(headers), expected_output)

    def test_parse_invalid_headers(self):
        """Test handling of malformed or irrelevant headers"""
        headers = {
            "x-oc-ratelimit-limit": "not-a-number",
            "some-other-header": "123",
        }

        expected_output: List[RateLimit] = []

        self.assertEqual(parse_rate_limit_headers(headers), expected_output)

    def test_parse_empty_headers(self):
        """Test handling of empty headers"""
        headers = {}

        expected_output: List[RateLimit] = []

        self.assertEqual(parse_rate_limit_headers(headers), expected_output)

    def test_parse_none_values(self):
        """Test handling of headers with None values"""
        headers = {
            "x-oc-ratelimit-limit": None,
            "x-oc-used-weight": "100",
        }

        expected_output: List[RateLimit] = [RateLimit(usedWeight=100)]

        self.assertEqual(parse_rate_limit_headers(headers), expected_output)
