"""
Tests for the API module.
"""

import unittest
from unittest.mock import Mock, patch

from copilot_model_sync.api import detect_api_endpoint, extract_base_url, fetch_models


class TestAPI(unittest.TestCase):
    """Test cases for the API module."""

    def test_extract_base_url_without_v1(self):
        """Test extracting base URL without /v1 suffix."""
        self.assertEqual(extract_base_url("http://localhost:8080"), "http://localhost:8080")
        self.assertEqual(extract_base_url("http://localhost:8080/"), "http://localhost:8080")

    def test_extract_base_url_with_v1(self):
        """Test extracting base URL with /v1 suffix."""
        self.assertEqual(extract_base_url("http://localhost:8080/v1"), "http://localhost:8080")
        self.assertEqual(extract_base_url("http://localhost:8080/v1/"), "http://localhost:8080")

    @patch('copilot_model_sync.api.requests.get')
    def test_detect_api_endpoint_success_v1(self, mock_get):
        """Test detecting API endpoint with successful /v1/models response."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = detect_api_endpoint("http://localhost:8080")
        self.assertEqual(result, "http://localhost:8080/v1/models")

    @patch('copilot_model_sync.api.requests.get')
    def test_detect_api_endpoint_fallback_to_models(self, mock_get):
        """Test detecting API endpoint falling back to /models."""
        # First call fails, second succeeds
        mock_get.side_effect = [
            Mock(**{'raise_for_status.side_effect': Exception("Not found")}),
            Mock(json=Mock(return_value={"data": []}), raise_for_status=Mock(return_value=None))
        ]

        result = detect_api_endpoint("http://localhost:8080")
        self.assertEqual(result, "http://localhost:8080/models")

    @patch('copilot_model_sync.api.requests.get')
    def test_detect_api_endpoint_failure(self, mock_get):
        """Test detecting API endpoint with all endpoints failing."""
        mock_get.side_effect = Exception("All endpoints failed")
        result = detect_api_endpoint("http://localhost:8080")
        self.assertIsNone(result)

    @patch('copilot_model_sync.api.requests.get')
    def test_fetch_models_success(self, mock_get):
        """Test fetching models successfully."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": [{"id": "test-model"}]}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fetch_models("http://localhost:8080/v1/models")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], "test-model")

    @patch('copilot_model_sync.api.requests.get')
    def test_fetch_models_failure(self, mock_get):
        """Test fetching models with request failure."""
        mock_get.side_effect = Exception("Network error")
        result = fetch_models("http://localhost:8080/v1/models")
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
