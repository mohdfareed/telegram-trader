#!/usr/bin/env sh
# Development Environment Setup Script
set -euo pipefail

echo "updating project: $*"
uv version --bump "$@"
echo "updating dependencies..."
uv lock --upgrade

tag_name="$(uv version --short)"
echo "updating repo to version: $tag_name"
git tag -f -a "v$tag_name" -m "version $tag_name"
git push origin "v$tag_name" --force
echo "update complete"
