#!/bin/bash
set -e

# shellcheck source=/dev/null
source ./.venv/bin/activate
# shellcheck source=/dev/null
source .env

uv run -m bot start
