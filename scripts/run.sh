#!/bin/bash
set -e

# TelegramTrader Bot - Test Runner
# Script to run formatters and tests with coverage

# shellcheck source=/dev/null
source ./.venv/bin/activate
# shellcheck source=/dev/null
source .env

uv run
