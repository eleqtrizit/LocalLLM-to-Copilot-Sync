"""
Utility functions for the copilot model updater.
"""

import os
import shutil
from datetime import datetime
from typing import Any, Dict

from rich.console import Console

console = Console()


def backup_settings_file(settings_path: str) -> str:
    """
    Create a timestamped backup of the settings file.

    :param settings_path: Path to the settings file
    :type settings_path: str
    :return: Path to the backup file
    :rtype: str
    """
    if not os.path.exists(settings_path):
        console.print(f"[yellow]Settings file not found, no backup needed:[/yellow] {settings_path}")
        return ""

    # Create timestamped backup filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{settings_path}.backup.{timestamp}"

    try:
        shutil.copy2(settings_path, backup_path)
        console.print(f"[green]Backup created:[/green] {backup_path}")
        return backup_path
    except Exception as e:
        console.print(f"[red]Failed to create backup:[/red] {e}")
        return ""


def validate_settings(settings: Dict[str, Any]) -> bool:
    """
    Validate that settings is a proper dictionary structure.

    :param settings: Settings dictionary to validate
    :type settings: Dict[str, Any]
    :return: True if valid, False otherwise
    :rtype: bool
    """
    return isinstance(settings, dict)
