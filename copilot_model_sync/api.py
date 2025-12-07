"""
API client for fetching models from OpenAI-compatible endpoints.
"""

from typing import Any, Dict, List, Optional

import requests
from rich.console import Console

console = Console()


def extract_base_url(host: str) -> str:
    """
    Extract the base URL from a host string, removing any trailing /v1 or /v1/ suffix.

    :param host: Host URL string
    :type host: str
    :return: Base URL without trailing /v1
    :rtype: str
    """
    # Remove trailing slashes
    host = host.rstrip('/')

    # Remove /v1 suffix if present
    if host.endswith('/v1'):
        host = host[:-3]

    return host


def detect_api_endpoint(base_url: str) -> Optional[str]:
    """
    Detect the correct API endpoint by testing /v1/models and /models.

    :param base_url: Base URL to test
    :type base_url: str
    :return: Detected endpoint URL or None if neither works
    :rtype: Optional[str]
    """
    # Test endpoints in order of preference
    endpoints = [
        f"{base_url.rstrip('/')}/v1/models",
        f"{base_url.rstrip('/')}/models"
    ]

    for endpoint in endpoints:
        try:
            console.print(f"[blue]Testing endpoint:[/blue] {endpoint}")
            response = requests.get(endpoint, timeout=10)
            response.raise_for_status()

            # Check if response is valid JSON with expected structure
            data = response.json()
            if isinstance(data, dict) and ('data' in data or 'models' in data):
                console.print(f"[green]Endpoint works:[/green] {endpoint}")
                return endpoint

        except Exception as e:
            console.print(f"[yellow]Endpoint failed:[/yellow] {endpoint} - {e}")
            continue

    return None


def fetch_models(endpoint: str) -> List[Dict[str, Any]]:
    """
    Fetch models from the detected API endpoint.

    :param endpoint: API endpoint URL
    :type endpoint: str
    :return: List of model dictionaries
    :rtype: List[Dict[str, Any]]
    """
    try:
        response = requests.get(endpoint, timeout=30)
        response.raise_for_status()

        data = response.json()

        # Handle different response formats
        if isinstance(data, dict):
            if 'data' in data:
                return data['data']
            elif 'models' in data:
                return data['models']
            else:
                # Assume the entire response is the model list
                return [data] if isinstance(data, dict) else data

        return data if isinstance(data, list) else []

    except Exception as e:
        console.print(f"[red]Error fetching models:[/red] {e}")
        return []


# Example usage for testing
if __name__ == "__main__":
    # Test with a sample endpoint
    test_url = "http://localhost:8080"
    base_url = extract_base_url(test_url)
    print(f"Base URL: {base_url}")

    endpoint = detect_api_endpoint(base_url)
    if endpoint:
        models = fetch_models(endpoint)
        print(f"Found {len(models)} models")
