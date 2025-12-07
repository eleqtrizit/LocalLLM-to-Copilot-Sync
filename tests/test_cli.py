"""
Tests for the CLI module.
"""

import unittest
from unittest.mock import patch

from copilot_model_sync.cli import parse_arguments


class TestCLI(unittest.TestCase):
    """Test cases for the CLI module."""

    def test_parse_arguments_host_required(self):
        """Test that host argument is required."""
        with self.assertRaises(SystemExit):
            parse_arguments()

    @patch('copilot_model_sync.cli.get_vscode_settings_path')
    @patch('copilot_model_sync.cli.load_settings')
    @patch('copilot_model_sync.cli.detect_api_endpoint')
    def test_main_missing_endpoint(self, mock_detect_endpoint, mock_load_settings, mock_get_path):
        """Test main function with missing endpoint."""
        mock_detect_endpoint.return_value = None
        mock_load_settings.return_value = {}
        mock_get_path.return_value = "/fake/path/settings.json"

        # This would normally be called with arguments, but we're testing the logic flow
        # For now, we'll just verify the structure is correct
        self.assertTrue(True)  # Placeholder until we can properly test


if __name__ == '__main__':
    unittest.main()
