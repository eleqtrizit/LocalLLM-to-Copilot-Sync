"""
Tests for the settings module.
"""

import json
import os
import tempfile
import unittest
from unittest.mock import patch

from copilot_model_sync.settings import get_vscode_settings_path, load_settings, save_settings


class TestSettings(unittest.TestCase):
    """Test cases for the settings module."""

    @patch('platform.system')
    @patch.dict(os.environ, {'APPDATA': 'C:\\Users\\test\\AppData\\Roaming'}, clear=True)
    def test_get_vscode_settings_path_windows(self, mock_system):
        """Test getting VSCode settings path on Windows."""
        mock_system.return_value = 'Windows'
        result = get_vscode_settings_path()
        expected_parts = ['C:', 'Users', 'test', 'AppData', 'Roaming', 'Code', 'User', 'settings.json']
        # Check that all parts are present in the result
        for part in expected_parts:
            self.assertIn(part, result)

    @patch('platform.system')
    @patch('os.path.expanduser')
    def test_get_vscode_settings_path_macos(self, mock_expanduser, mock_system):
        """Test getting VSCode settings path on macOS."""
        mock_system.return_value = 'Darwin'
        mock_expanduser.return_value = '/Users/test'
        expected = '/Users/test/Library/Application Support/Code/User/settings.json'
        result = get_vscode_settings_path()
        self.assertEqual(result, expected)

    @patch('platform.system')
    @patch('os.path.expanduser')
    def test_get_vscode_settings_path_linux(self, mock_expanduser, mock_system):
        """Test getting VSCode settings path on Linux."""
        mock_system.return_value = 'Linux'
        mock_expanduser.return_value = '/home/test'
        expected = '/home/test/.config/Code/User/settings.json'
        result = get_vscode_settings_path()
        self.assertEqual(result, expected)

    @patch('platform.system')
    def test_get_vscode_settings_path_unsupported(self, mock_system):
        """Test getting VSCode settings path on unsupported platform."""
        mock_system.return_value = 'Unsupported'
        with self.assertRaises(RuntimeError):
            get_vscode_settings_path()

    def test_load_settings_file_not_found(self):
        """Test loading settings from non-existent file."""
        with self.assertRaises(FileNotFoundError):
            load_settings("/nonexistent/path/settings.json")

    def test_load_settings_success(self):
        """Test successfully loading settings from file."""
        # Create a temporary file with JSON content
        test_data = {"test": "value"}
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
            json.dump(test_data, temp_file)
            temp_path = temp_file.name

        try:
            result = load_settings(temp_path)
            self.assertEqual(result, test_data)
        finally:
            os.remove(temp_path)

    def test_save_settings_success(self):
        """Test successfully saving settings to file."""
        test_data = {"test": "value"}
        with tempfile.TemporaryDirectory() as temp_dir:
            settings_path = os.path.join(temp_dir, "settings.json")
            save_settings(settings_path, test_data)

            # Verify the file was created and contains the correct data
            with open(settings_path, 'r') as f:
                saved_data = json.load(f)
            self.assertEqual(saved_data, test_data)


if __name__ == '__main__':
    unittest.main()
