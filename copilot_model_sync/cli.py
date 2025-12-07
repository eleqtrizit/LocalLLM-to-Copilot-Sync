"""
Command line interface for the copilot model updater.
"""

import argparse
import sys

from rich.console import Console

from .api import detect_api_endpoint, fetch_models
from .models import apply_update_logic, compare_models
from .settings import get_vscode_settings_path, load_settings, save_settings
from .utils import backup_settings_file

console = Console()


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.

    :return: Parsed arguments
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        description="Update GitHub Copilot custom models in VSCode settings"
    )
    parser.add_argument(
        "--host",
        required=True,
        help="Host URL (e.g., http://localhost:8080 or http://localhost:8080/v1)"
    )
    parser.add_argument(
        "--insiders",
        action="store_true",
        help="Use VSCode Insiders instead of regular VSCode"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what changes would be made without actually modifying settings"
    )
    parser.add_argument(
        "--api-key-required",
        action="store_true",
        help="Set requiresAPIKey=true for all models with the same base URL, overriding any previous settings"
    )

    return parser.parse_args()


def main() -> int:
    """
    Main entry point for the copilot model updater.

    :return: Exit code (0 for success, 1 for error)
    :rtype: int
    """
    try:
        args = parse_arguments()

        # Get VSCode settings path
        settings_path = get_vscode_settings_path(args.insiders)
        console.print(f"[blue]Using settings file:[/blue] {settings_path}")

        # Load current settings
        try:
            settings = load_settings(settings_path)
        except FileNotFoundError:
            console.print("[yellow]Settings file not found, creating new one[/yellow]")
            settings = {}
        except Exception as e:
            console.print(f"[red]Error loading settings:[/red] {e}")
            return 1

        # Detect API endpoint
        console.print(f"[blue]Detecting API endpoint for:[/blue] {args.host}")
        endpoint = detect_api_endpoint(args.host)
        if not endpoint:
            console.print("[red]Failed to detect API endpoint[/red]")
            return 1

        console.print(f"[green]Found API endpoint:[/green] {endpoint}")

        # Fetch models from API
        console.print("[blue]Fetching models from API...[/blue]")
        api_models = fetch_models(endpoint)
        if not api_models:
            console.print("[red]Failed to fetch models from API[/red]")
            return 1

        console.print(f"[green]Found {len(api_models)} models in API[/green]")

        # Get current models from settings
        current_models = settings.get("github.copilot.chat.customOAIModels", {})
        disabled_models = settings.get("github.copilot.chat.customOAIModels.disabled", {})

        console.print(f"[blue]Current active models:[/blue] {len(current_models)}")
        console.print(f"[blue]Currently disabled models:[/blue] {len(disabled_models)}")

        # Compare models
        comparisons = compare_models(current_models, disabled_models, api_models)

        # Display comparison results
        if comparisons["matching"]:
            console.print(f"[green]Matching models (unchanged):[/green] {len(comparisons['matching'])}")
        if comparisons["obsolete"]:
            console.print(f"[yellow]Obsolete models (to disable):[/yellow] {len(comparisons['obsolete'])}")
        if comparisons["to_reenable"]:
            console.print(f"[cyan]Models to re-enable:[/cyan] {len(comparisons['to_reenable'])}")
        if comparisons["new_models"]:
            console.print(f"[blue]New models (to add):[/blue] {len(comparisons['new_models'])}")

        # Apply update logic
        updated_settings = apply_update_logic(settings, comparisons, args.host, args.api_key_required)

        # Save updated settings
        if args.dry_run:
            console.print("[yellow]DRY RUN: Would save the following changes:[/yellow]")
            import json
            console.print(json.dumps(updated_settings, indent=2))
        else:
            # Create backup
            backup_path = backup_settings_file(settings_path)
            console.print(f"[blue]Created backup:[/blue] {backup_path}")

            # Save settings
            save_settings(settings_path, updated_settings)
            console.print("[green]Settings updated successfully![/green]")

        return 0

    except KeyboardInterrupt:
        console.print("[yellow]Operation cancelled by user[/yellow]")
        return 1
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
