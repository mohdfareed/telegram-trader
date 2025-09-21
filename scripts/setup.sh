#!/usr/bin/env sh
# Development Environment Setup Script
set -euo pipefail

# Check if uv is installed
if ! command -v uv >/dev/null 2>&1; then
    echo "uv is not installed, install from:" >&2
    echo "https://docs.astral.sh/uv/getting-started/installation" >&2
    exit 1
fi

# Create virtual environment
echo "setting up venv with Python $PYTHON_VERSION..."
uv venv ./.venv --clear

# Install development dependencies
echo "installing development dependencies..."
uv pip install --upgrade pip
uv sync
