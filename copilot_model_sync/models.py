"""
Model comparison and update logic for GitHub Copilot custom models.
"""

from typing import Any, Dict, List

from rich.console import Console
from rich.prompt import Prompt

console = Console()


def compare_models(current_models: Dict[str, Any], disabled_models: Dict[str, Any],
                   api_models: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """
    Compare current models with API models to determine what needs to be updated.

    :param current_models: Current active models from settings
    :type current_models: Dict[str, Any]
    :param disabled_models: Currently disabled models from settings
    :type disabled_models: Dict[str, Any]
    :param api_models: Models fetched from API
    :type api_models: List[Dict[str, Any]]
    :return: Dictionary with model categories
    :rtype: Dict[str, List[str]]
    """
    # Extract model IDs from API models, filtering out None values
    api_model_ids = set()
    for model in api_models:
        model_id = model.get('id') or model.get('name')
        if model_id is not None:
            api_model_ids.add(str(model_id))

    current_model_ids = set(current_models.keys())
    disabled_model_ids = set(disabled_models.keys())

    # Models that exist in both current settings and API (no change needed)
    matching = list(current_model_ids.intersection(api_model_ids))

    # Models that exist in current settings but not in API (should be disabled)
    obsolete = list(current_model_ids.difference(api_model_ids))

    # Models that exist in disabled section but are in API (should be re-enabled)
    to_reenable = list(disabled_model_ids.intersection(api_model_ids))

    # Models that exist in API but not in either current or disabled (new models)
    new_models = list(api_model_ids.difference(current_model_ids.union(disabled_model_ids)))

    return {
        'matching': sorted(matching, key=str.lower),
        'obsolete': sorted(obsolete, key=str.lower),
        'to_reenable': sorted(to_reenable, key=str.lower),
        'new_models': sorted(new_models, key=str.lower)
    }


def prompt_for_model_params(model_id: str, base_url: str, api_key_required: bool = False) -> Dict[str, Any]:
    """
    Prompt user for model parameters for a new model.

    :param model_id: Model identifier
    :type model_id: str
    :param base_url: Base URL for the model
    :type base_url: str
    :param api_key_required: Whether to set requiresAPIKey=true for this model
    :type api_key_required: bool
    :return: Model configuration dictionary
    :rtype: Dict[str, Any]
    """
    console.print(f"\n[yellow]New model found:[/yellow] {model_id}")

    # Use smart defaults
    model_config = {
        'name': model_id,
        'url': f"{base_url.rstrip('/')}/v1/chat/completions",
        'toolCalling': True,
        'vision': False,
        'thinking': True,
        'maxInputTokens': 128000,
        'maxOutputTokens': 4096,
        'requiresAPIKey': api_key_required  # Set based on the flag
    }

    # Allow user to customize or accept defaults
    for key, default_value in model_config.items():
        if key in ['name', 'url']:
            # These are critical, always prompt
            value = Prompt.ask(f"  {key}", default=str(default_value))
            model_config[key] = value if key != 'requiresAPIKey' else value.lower() == 'true'
        else:
            # For other parameters, show default and allow skipping
            value = Prompt.ask(f"  {key} (default: {default_value})", default=str(default_value))
            # Convert string values to appropriate types
            if key in ['toolCalling', 'vision', 'thinking', 'requiresAPIKey']:
                model_config[key] = value.lower() in ['true', '1', 'yes', 'y']
            elif key in ['maxInputTokens', 'maxOutputTokens']:
                try:
                    model_config[key] = int(value)
                except ValueError:
                    model_config[key] = default_value

    return model_config


def apply_update_logic(settings: Dict[str, Any], comparisons: Dict[str, List[str]],
                       base_url: str, api_key_required: bool = False) -> Dict[str, Any]:
    """
    Apply the update logic to modify settings based on model comparisons.

    :param settings: Current VSCode settings
    :type settings: Dict[str, Any]
    :param comparisons: Model comparison results
    :type comparisons: Dict[str, List[str]]
    :param base_url: Base URL for API
    :type base_url: str
    :param api_key_required: Whether to set requiresAPIKey=true for all models with same base URL
    :type api_key_required: bool
    :return: Updated settings
    :rtype: Dict[str, Any]
    """
    # Make a copy of settings to avoid modifying the original
    updated_settings = settings.copy()

    # Ensure the custom models sections exist
    if 'github.copilot.chat.customOAIModels' not in updated_settings:
        updated_settings['github.copilot.chat.customOAIModels'] = {}

    if 'github.copilot.chat.customOAIModels.disabled' not in updated_settings:
        updated_settings['github.copilot.chat.customOAIModels.disabled'] = {}

    current_models = updated_settings['github.copilot.chat.customOAIModels']
    disabled_models = updated_settings['github.copilot.chat.customOAIModels.disabled']

    # If api_key_required is True, set requiresAPIKey for all models with the same base URL
    if api_key_required:
        # Process active models
        for model_id, model_config in current_models.items():
            # Check if the model's URL matches the base URL
            model_url = model_config.get('url', '')
            if model_url.startswith(base_url.rstrip('/')):
                console.print(f"[cyan]Setting requiresAPIKey=true for model:[/cyan] {model_id}")
                model_config['requiresAPIKey'] = True

        # Process disabled models
        for model_id, model_config in disabled_models.items():
            # Check if the model's URL matches the base URL
            model_url = model_config.get('url', '')
            if model_url.startswith(base_url.rstrip('/')):
                console.print(f"[cyan]Setting requiresAPIKey=true for disabled model:[/cyan] {model_id}")
                model_config['requiresAPIKey'] = True

    # 1. Move obsolete models to disabled section
    for model_id in comparisons['obsolete']:
        if model_id in current_models:
            console.print(f"[yellow]Disabling obsolete model:[/yellow] {model_id}")
            disabled_models[model_id] = current_models.pop(model_id)

    # 2. Move re-enabled models back to active section
    for model_id in comparisons['to_reenable']:
        if model_id in disabled_models:
            console.print(f"[green]Re-enabling model:[/green] {model_id}")
            current_models[model_id] = disabled_models.pop(model_id)

    # 3. Add new models (this would normally prompt user, but for now we'll use defaults)
    # In a real implementation, we'd prompt the user here
    for model_id in comparisons['new_models']:
        console.print(f"[blue]Adding new model:[/blue] {model_id}")
        # For demo purposes, we'll create a basic config
        # In practice, this would call prompt_for_model_params
        new_model_config = {
            'name': model_id,
            'url': f"{base_url.rstrip('/')}/v1/chat/completions",
            'toolCalling': True,
            'vision': False,
            'thinking': True,
            'maxInputTokens': 128000,
            'maxOutputTokens': 4096,
            'requiresAPIKey': api_key_required  # Set based on the flag
        }
        current_models[model_id] = new_model_config

    # 4. Matching models remain unchanged (no action needed)
    # But if api_key_required is True, we still need to update their requiresAPIKey setting
    if api_key_required:
        for model_id in comparisons['matching']:
            if model_id in current_models:
                model_config = current_models[model_id]
                model_url = model_config.get('url', '')
                if model_url.startswith(base_url.rstrip('/')):
                    console.print(f"[cyan]Setting requiresAPIKey=true for existing model:[/cyan] {model_id}")
                    model_config['requiresAPIKey'] = True

    return updated_settings
