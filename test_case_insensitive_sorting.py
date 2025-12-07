#!/usr/bin/env python3
"""
Test script to demonstrate case-insensitive sorting of models.
"""

from copilot_model_sync.models import compare_models


def test_case_insensitive_sorting():
    """Test that model lists are sorted case-insensitively."""
    # Sample current models with mixed case
    current_models = {
        "GPT-4": {},
        "claude-2": {},
        "gpt-3.5-turbo": {}
    }

    # Sample disabled models with mixed case
    disabled_models = {
        "CLAUDE-3-OPUS": {},
        "llama-2": {}
    }

    # Sample API models with mixed case
    api_models = [
        {"id": "GPT-4"},           # Existing model - no change
        {"id": "claude-3-opus"},   # Disabled model - should be re-enabled
        {"id": "llama-2"},         # Disabled model - should be re-enabled
        {"id": "GPT-4-TURBO"},     # New model
        {"id": "claude-3-sonnet"}  # New model
    ]

    # Compare models
    comparisons = compare_models(current_models, disabled_models, api_models)

    print("Case-Insensitive Sorting Test Results:")
    print("=" * 50)
    print(f"Matching models: {comparisons['matching']}")
    print(f"Obsolete models: {comparisons['obsolete']}")
    print(f"Models to re-enable: {comparisons['to_reenable']}")
    print(f"New models: {comparisons['new_models']}")

    # Verify that all lists are sorted case-insensitively
    def is_sorted_case_insensitive(lst):
        """Check if a list is sorted case-insensitively."""
        lower_list = [item.lower() for item in lst]
        return lower_list == sorted(lower_list)

    print("\nVerification:")
    print("=" * 50)
    print(f"Matching models sorted case-insensitively: {is_sorted_case_insensitive(comparisons['matching'])}")
    print(f"Obsolete models sorted case-insensitively: {is_sorted_case_insensitive(comparisons['obsolete'])}")
    print(f"Models to re-enable sorted case-insensitively: {is_sorted_case_insensitive(comparisons['to_reenable'])}")
    print(f"New models sorted case-insensitively: {is_sorted_case_insensitive(comparisons['new_models'])}")

    # Show the actual sorting behavior
    print("\nDetailed Analysis:")
    print("=" * 50)
    print("Obsolete models (should be sorted case-insensitively):")
    print("  Actual:", comparisons['obsolete'])
    print("  Lowercase:", [m.lower() for m in comparisons['obsolete']])
    print("  Sorted lowercase:", sorted([m.lower() for m in comparisons['obsolete']]))

    print("\nModels to re-enable (should be sorted case-insensitively):")
    print("  Actual:", comparisons['to_reenable'])

    print("\nNew models (should be sorted case-insensitively):")
    print("  Actual:", comparisons['new_models'])
    print("  Lowercase:", [m.lower() for m in comparisons['new_models']])
    print("  Sorted lowercase:", sorted([m.lower() for m in comparisons['new_models']]))


if __name__ == "__main__":
    test_case_insensitive_sorting()
