#!/bin/bash
set -e

# TelegramTrader Bot - Update Script
# Script to update development dependencies

# shellcheck source=/dev/null
source ./.venv/bin/activate

# uv
echo "updating project dependencies..."
uv lock --upgrade
