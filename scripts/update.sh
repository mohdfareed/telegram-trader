#!/usr/bin/env sh
# Development Environment Setup Script
set -euo pipefail

# bump version and update dependencies
echo "updating project version: $*"
uv version --bump "$@"
echo "updating dependencies..."
uv lock --upgrade

# commit changes
echo "committing changes..."
git add pyproject.toml uv.lock
tag_name="$(uv version --short)"
git commit -m "chore(release): v${tag_name}"

# tag and push changes
echo "tagging repo: v${tag_name}"
git tag -a "v${tag_name}" -m "version ${tag_name}"
git push origin HEAD "v${tag_name}"

# docker instructions
echo "update complete"
echo "run 'scripts/deploy.sh' to push docker image"
