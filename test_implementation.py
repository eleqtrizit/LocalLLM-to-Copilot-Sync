#!/usr/bin/env python3
"""
Test script for copilot model sync functionality.
"""

import json
import os
import tempfile

from copilot_model_sync.api import extract_base_url
from copilot_model_sync.models import compare_models
from copilot_model_sync.settings import load_settings, save_settings
from copilot_model_sync.utils import validate_settings


def test_extract_base_url():
    """Test URL extraction functionality."""
    print("Testing URL extraction...")
    assert extract_base_url("http://localhost:8080") == "http://localhost:8080"
    assert extract_base_url("http://localhost:8080/") == "http://localhost:8080"
    assert extract_base_url("http://localhost:8080/v1") == "http://localhost:8080"
    assert extract_base_url("http://localhost:8080/v1/") == "http://localhost:8080"
    print("✓ URL extraction tests passed")


def test_model_comparison():
    """Test model comparison logic."""
    print("Testing model comparison...")

    current_models = {
        "gpt-4": {"name": "gpt-4", "url": "https://api.openai.com/v1/chat/completions"},
        "gpt-3.5-turbo": {"name": "gpt-3.5-turbo", "url": "https://api.openai.com/v1/chat/completions"}
    }

    disabled_models = {
        "claude-2": {"name": "claude-2", "url": "https://api.anthropic.com/v1/complete"}
    }

    api_models = [
        {"id": "gpt-4"},  # Matching model
        {"id": "gpt-4-turbo"},  # New model
        {"id": "claude-2"}  # Model to re-enable
    ]

    comparisons = compare_models(current_models, disabled_models, api_models)

    assert "gpt-4" in comparisons["matching"]
    assert "gpt-3.5-turbo" in comparisons["obsolete"]
    assert "claude-2" in comparisons["to_reenable"]
    assert len(comparisons["new_models"]) == 1  # gpt-4-turbo

    print("✓ Model comparison tests passed")


def test_settings_operations():
    """Test settings file operations."""
    print("Testing settings operations...")

    # Test with temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        test_settings = {
            "editor.fontSize": 14,
            "github.copilot.chat.customOAIModels": {
                "test-model": {"name": "test-model", "url": "http://localhost:8080/v1/chat/completions"}
            }
        }
        json.dump(test_settings, f)
        temp_path = f.name

    try:
        # Test loading
        loaded_settings = load_settings(temp_path)
        assert loaded_settings["editor.fontSize"] == 14

        # Test saving
        loaded_settings["editor.fontSize"] = 16
        save_settings(temp_path, loaded_settings)

        # Verify save worked
        reloaded_settings = load_settings(temp_path)
        assert reloaded_settings["editor.fontSize"] == 16

        print("✓ Settings operations tests passed")

    finally:
        os.unlink(temp_path)


def test_validation():
    """Test settings validation."""
    print("Testing validation...")

    assert validate_settings({"key": "value"}) is True
    assert validate_settings("not a dict") is False
    assert validate_settings(None) is False
    assert validate_settings([]) is False

    print("✓ Validation tests passed")


def run_all_tests():
    """Run all tests."""
    print("Running all tests...\n")

    test_extract_base_url()
    test_model_comparison()
    test_settings_operations()
    test_validation()

    print("\n🎉 All tests passed!")


if __name__ == "__main__":
    run_all_tests()
