# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python tool called "Copilot Model Sync" that automatically synchronizes custom AI models with GitHub Copilot in VSCode. The tool detects available models from OpenAI-compatible API endpoints and intelligently updates VSCode Copilot configuration based on API availability.

## Key Features

- Automatic Model Discovery: Detects available models from OpenAI-compatible API endpoints
- Smart Synchronization: Intelligently updates VSCode Copilot configuration based on API availability
- Safe Updates: Creates backups before making changes and supports dry-run mode
- Cross-Platform: Works on Windows, macOS, and Linux
- VSCode & Insiders: Supports both regular VSCode and VSCode Insiders

## Project Structure

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
└── README.md                   # Documentation
```

## Core Architecture

The application follows a modular architecture with clear separation of concerns:

1. **CLI Layer** (`cli.py`): Handles command-line argument parsing and user interaction
2. **API Layer** (`api.py`): Manages communication with OpenAI-compatible endpoints
3. **Model Logic Layer** (`models.py`): Implements model comparison and update logic
4. **Settings Layer** (`settings.py`): Handles VSCode settings file operations
5. **Utilities Layer** (`utils.py`): Provides helper functions like backup creation

## Development Commands

### Setup
```bash
# Create virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e .

# Install development dependencies
pip install pytest pytest-cov
```

### Common Development Tasks
```bash
# Run all tests
make test

# Run linter
make lint

# Format code
make format

# Clean build artifacts
make clean
```

## Testing

Tests are written using pytest and organized by module:
- `test_api.py`: Tests for API client functionality
- `test_cli.py`: Tests for command-line interface
- `test_models.py`: Tests for model comparison logic
- `test_settings.py`: Tests for settings file operations
- `test_utils.py`: Tests for utility functions

Run tests with: `make test` or `pytest tests/ -v`

## Build and Distribution

Build distribution packages with: `make build` or `python -m build`

## Key Dependencies

- `requests`: For HTTP API calls
- `rich`: For enhanced terminal output
- `json5`: For parsing VSCode settings files
- `pytest`: For testing

## Entry Points

The main entry point is `copilot_model_sync/__main__.py`, which delegates to `cli.py`.

## Configuration

The tool modifies these sections in VSCode `settings.json`:
- `github.copilot.chat.customOAIModels` - Active custom models
- `github.copilot.chat.customOAIModels.disabled` - Disabled custom models
