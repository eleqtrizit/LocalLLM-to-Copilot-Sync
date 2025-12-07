"""
Tests for the utils module.
"""

import os
import tempfile
import unittest

from copilot_model_sync.utils import backup_settings_file, validate_settings


class TestUtils(unittest.TestCase):
    """Test cases for the utils module."""

    def test_validate_settings_valid_dict(self):
        """Test validating a valid settings dictionary."""
        valid_settings = {"key": "value"}
        self.assertTrue(validate_settings(valid_settings))

    def test_validate_settings_invalid_type(self):
        """Test validating an invalid settings type."""
        self.assertFalse(validate_settings("not a dict"))
        self.assertFalse(validate_settings(None))
        self.assertFalse(validate_settings([]))

    def test_backup_settings_file_not_found(self):
        """Test backing up a non-existent settings file."""
        result = backup_settings_file("/nonexistent/path/settings.json")
        self.assertEqual(result, "")

    def test_backup_settings_file_success(self):
        """Test successfully backing up a settings file."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write('{"test": "data"}')
            temp_path = temp_file.name

        try:
            # Test backup
            backup_path = backup_settings_file(temp_path)
            self.assertTrue(os.path.exists(backup_path))

            # Clean up backup
            os.remove(backup_path)
        finally:
            # Clean up temp file
            os.remove(temp_path)


if __name__ == '__main__':
    unittest.main()
