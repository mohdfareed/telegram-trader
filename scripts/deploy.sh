#!/usr/bin/env sh
# Deploy bot container
set -euo pipefail

USERNAME="mohdfareed"
IMAGE_NAME="telegram-trader"

image_url="ghcr.io/$USERNAME/$IMAGE_NAME"
github_token="${GITHUB_TOKEN:-$GITHUB_REGISTRY_TOKEN}"

# authenticate to github container registry
echo "authenticating to github container registry..."
echo "$github_token" | docker login ghcr.io -u $USERNAME --password-stdin

# get new version
tag="$(uv version --short)"
echo "deploying version: $tag"

# build image
echo "building image..."
docker build -t $IMAGE_NAME:"${tag}" . --no-cache

# deploy image to registry
echo "pushing image to github..."
docker tag $IMAGE_NAME:"${tag}" $image_url:"${tag}"
docker push $image_url:"${tag}"

# tag and push as latest
echo "tagging build as latest..."
docker tag $IMAGE_NAME:"${tag}" $image_url:latest
docker push $image_url:latest
