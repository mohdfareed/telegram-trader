#!/bin/bash
set -e

# shellcheck source=/dev/null
source ./.venv/bin/activate

echo "updating project dependencies..."
uv lock --upgrade
