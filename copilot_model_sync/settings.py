"""
VSCode settings file operations for GitHub Copilot configuration.
"""

import json
import os
import platform
from typing import Any, Dict

import json5
from rich.console import Console

console = Console()


def get_vscode_settings_path(insiders: bool = False) -> str:
    """
    Get the platform-specific path to VSCode settings.json file.

    :param insiders: Whether to use VSCode Insiders path
    :type insiders: bool
    :return: Path to settings.json file
    :rtype: str
    :raises RuntimeError: If unable to determine settings path for the platform
    """
    folder_name = "Code - Insiders" if insiders else "Code"

    system = platform.system()
    if system == "Windows":
        appdata = os.environ.get('APPDATA')
        if not appdata:
            raise RuntimeError("APPDATA environment variable not found on Windows")
        return os.path.join(appdata, folder_name, "User", "settings.json")

    elif system == "Darwin":  # macOS
        home = os.path.expanduser("~")
        return os.path.join(home, "Library", "Application Support", folder_name, "User", "settings.json")

    elif system == "Linux":
        home = os.path.expanduser("~")
        return os.path.join(home, ".config", folder_name, "User", "settings.json")

    else:
        raise RuntimeError(f"Unsupported platform: {system}")


def load_settings(settings_path: str) -> Dict[str, Any]:
    """
    Load VSCode settings from JSON file.

    :param settings_path: Path to settings.json file
    :type settings_path: str
    :return: Settings dictionary
    :rtype: Dict[str, Any]
    :raises FileNotFoundError: If settings file doesn't exist
    :raises json5.decoder.Json5DecoderException: If settings file contains invalid JSON
    """
    if not os.path.exists(settings_path):
        raise FileNotFoundError(f"Settings file not found: {settings_path}")

    with open(settings_path, 'r', encoding='utf-8') as f:
        return json5.load(f)


def save_settings(settings_path: str, settings: Dict[str, Any]) -> None:
    """
    Save VSCode settings to JSON file.

    :param settings_path: Path to settings.json file
    :type settings_path: str
    :param settings: Settings dictionary to save
    :type settings: Dict[str, Any]
    :raises OSError: If unable to write to file
    :raises TypeError: If settings contains non-serializable objects
    """
    # Ensure directory exists
    settings_dir = os.path.dirname(settings_path)
    os.makedirs(settings_dir, exist_ok=True)

    with open(settings_path, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)
