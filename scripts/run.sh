#!/bin/bash
set -e

# Trade Poster Bot - Test Runner
# Script to run formatters and tests with coverage

# shellcheck source=/dev/null
source ./.venv/bin/activate
# shellcheck source=/dev/null
source .env

if [ "$DEBUG" = "true" ]; then
    uv run -d
else
    uv run
fi
