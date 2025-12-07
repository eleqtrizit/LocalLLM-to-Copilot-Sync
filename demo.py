#!/usr/bin/env python3
"""
Demonstration script showing how to use the copilot model sync tool.
"""

from copilot_model_sync.models import apply_update_logic, compare_models


def demo_with_sample_data():
    """Demonstrate the tool with sample data."""
    print("🚀 Copilot Model Sync - Demonstration")
    print("=" * 50)

    # Sample current settings
    current_settings = {
        "editor.fontSize": 14,
        "github.copilot.chat.customOAIModels": {
            "gpt-4": {
                "name": "gpt-4",
                "url": "https://api.openai.com/v1/chat/completions",
                "toolCalling": True,
                "vision": False,
                "thinking": True,
                "maxInputTokens": 128000,
                "maxOutputTokens": 4096,
                "requiresAPIKey": True
            },
            "gpt-3.5-turbo": {
                "name": "gpt-3.5-turbo",
                "url": "https://api.openai.com/v1/chat/completions",
                "toolCalling": True,
                "vision": False,
                "thinking": True,
                "maxInputTokens": 16385,
                "maxOutputTokens": 4096,
                "requiresAPIKey": True
            }
        },
        "github.copilot.chat.customOAIModels.disabled": {
            "claude-2": {
                "name": "claude-2",
                "url": "https://api.anthropic.com/v1/messages",
                "toolCalling": True,
                "vision": False,
                "thinking": True,
                "maxInputTokens": 100000,
                "maxOutputTokens": 4096,
                "requiresAPIKey": True
            }
        }
    }

    # Sample API models response
    api_models = [
        {"id": "gpt-4"},           # Existing model - no change
        {"id": "gpt-4-turbo"},     # New model
        {"id": "claude-3-opus"},   # New model
        {"id": "claude-2"}         # Disabled model - should be re-enabled
    ]

    print("📋 Current Settings:")
    print(f"  Active models: {len(current_settings['github.copilot.chat.customOAIModels'])}")
    print(f"  Disabled models: {len(current_settings['github.copilot.chat.customOAIModels.disabled'])}")

    print("\n🌐 API Models Found:")
    sorted_api_models = sorted(api_models, key=lambda x: x['id'].lower())
    for model in sorted_api_models:
        print(f"  - {model['id']}")

    # Compare models
    current_models = current_settings["github.copilot.chat.customOAIModels"]
    disabled_models = current_settings["github.copilot.chat.customOAIModels.disabled"]

    comparisons = compare_models(current_models, disabled_models, api_models)

    print("\n📊 Model Comparison Results:")
    print(f"  Matching models: {comparisons['matching']}")
    print(f"  Obsolete models: {comparisons['obsolete']}")
    print(f"  Models to re-enable: {comparisons['to_reenable']}")
    print(f"  New models: {comparisons['new_models']}")

    # Apply update logic
    updated_settings = apply_update_logic(current_settings.copy(), comparisons, "http://localhost:8080")

    print("\n🔄 Updated Settings:")
    print(f"  Active models: {len(updated_settings['github.copilot.chat.customOAIModels'])}")
    print(f"  Disabled models: {len(updated_settings['github.copilot.chat.customOAIModels.disabled'])}")

    # Show what changed
    print("\n📝 Changes Made:")
    if comparisons["obsolete"]:
        print("  Disabled models:")
        for model in comparisons["obsolete"]:
            print(f"    - {model}")

    if comparisons["to_reenable"]:
        print("  Re-enabled models:")
        for model in comparisons["to_reenable"]:
            print(f"    + {model}")

    if comparisons["new_models"]:
        print("  New models to add:")
        for model in comparisons["new_models"]:
            print(f"    + {model}")

    print("\n✅ Demonstration completed successfully!")
    print("\n💡 To use the actual tool:")
    print("   python -m copilot_model_sync --host http://localhost:8080")
    print("   python -m copilot_model_sync --host http://localhost:8080 --insiders")
    print("   python -m copilot_model_sync --host http://localhost:8080 --dry-run")


if __name__ == "__main__":
    demo_with_sample_data()
