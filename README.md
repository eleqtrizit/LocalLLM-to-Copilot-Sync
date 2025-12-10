# Copilot Model Sync

A Python tool to automatically synchronize custom AI models with GitHub Copilot in VSCode.

## Features

- **Automatic Model Discovery**: Automatically detects available models from OpenAI-compatible API endpoints
- **Smart Synchronization**: Intelligently updates your VSCode Copilot configuration based on API availability
- **Safe Updates**: Creates backups before making changes and supports dry-run mode
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **VSCode & Insiders**: Supports both regular VSCode and VSCode Insiders

## Installation

Install uv:
https://docs.astral.sh/uv/getting-started/installation/#installation-methods

```bash
uv tool install git+https://github.com/eleqtrizit/LocalLLM-to-Copilot-Sync
```

## Usage

### Basic Usage

```bash
# Sync models from a local API server
python -m copilot_model_sync --host http://localhost:8080

# Sync models from an API server with /v1 endpoint
python -m copilot_model_sync --host http://localhost:8080/v1

# Use VSCode Insiders instead of regular VSCode
python -m copilot_model_sync --host http://localhost:8080 --insiders

# Preview changes without actually making them
python -m copilot_model_sync --host http://localhost:8080 --dry-run

# Set requiresAPIKey=true for all models with the same base URL
python -m copilot_model_sync --host http://localhost:8080 --api-key-required

# Use API key for authentication with the API endpoint
python -m copilot_model_sync --host http://localhost:8080 --api-key YOUR_API_KEY_HERE
```

### Update Logic

The tool follows these rules when synchronizing models:

1. **Matching Models**: Models present in both your current configuration and the API remain unchanged
2. **Obsolete Models**: Models in your configuration but not in the API are moved to the disabled section
3. **Re-enable Models**: Models in the disabled section but available in the API are re-enabled
4. **New Models**: Models available in the API but not in your configuration are added (with default parameters)

### API Key Authentication

When using the `--api-key` flag, the tool will authenticate with the API endpoint using Bearer token authentication. This is useful when working with API endpoints that require authentication.

The API key is passed in the `Authorization` header as `Bearer YOUR_API_KEY_HERE`.

Note: The `--api-key` flag is for authenticating with the API endpoint, while the `--api-key-required` flag is for setting the `requiresAPIKey=true` parameter in the VSCode configuration for your models.

### API Key Requirement

When using the `--api-key-required` flag, the tool will set `requiresAPIKey=true` for all models that have the same base URL as specified in the `--host` parameter. This overrides any previous settings for those models. Models with different base URLs will remain unchanged.

## How It Works

1. **Endpoint Detection**: Automatically detects whether to use `/v1/models` or `/models` endpoints
2. **Model Comparison**: Compares your current VSCode settings with available API models
3. **Smart Updates**: Applies the update logic described above
4. **Backup Creation**: Creates timestamped backups before making changes
5. **Settings Update**: Safely updates your VSCode configuration

## Configuration

The tool modifies the following sections in your VSCode `settings.json`:

- `github.copilot.chat.customOAIModels` - Active custom models
- `github.copilot.chat.customOAIModels.disabled` - Disabled custom models

## Development

### Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Install development dependencies
pip install pytest pytest-cov
```

### Testing

```bash
# Run all tests
make test

# Run linter
make lint

# Format code
make format
```

### Project Structure

```
copilot_model_sync/
├── copilot_model_sync/          # Main package
│   ├── __init__.py             # Package initialization
│   ├── __main__.py             # Entry point
│   ├── cli.py                  # Command line interface
│   ├── api.py                  # API client functionality
│   ├── models.py               # Model comparison logic
│   ├── settings.py             # Settings file operations
│   └── utils.py                # Utility functions
├── tests/                      # Test files
├── demo.py                     # Demonstration script
├── pyproject.toml              # Project configuration
├── Makefile                    # Build commands
└── README.md                   # This file
```

## Requirements

- Python 3.11+
- VSCode with GitHub Copilot extension
- Access to OpenAI-compatible API endpoints

## License

MIT License - see LICENSE file for details.