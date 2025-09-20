#!/bin/sh
# Deploy bot container
set -e  # exit on any error

IMAGE_NAME="telegram-trader"
USERNAME="mohdfareed"
IMAGE_URL="ghcr.io/$USERNAME/$IMAGE_NAME"

# shellcheck source=/dev/null
source .env # load env variables

# authenticate to github container registry
echo "authenticating to github container registry..."
echo "$GITHUB_TOKEN" | docker login ghcr.io -u $USERNAME --password-stdin

# get new version
tag="$(uv version --short)"
echo "deploying version: $tag"

# build image
echo "building image..."
docker build -t $IMAGE_NAME:"${tag}" . --no-cache

# deploy image to registry
echo "pushing image to github..."
docker tag $IMAGE_NAME:"${tag}" $IMAGE_URL:"${tag}"
docker push $IMAGE_URL:"${tag}"

# tag and push latest if not already latest
echo "tagging build as latest..."
docker tag $IMAGE_NAME:"${tag}" $IMAGE_URL:latest
docker push $IMAGE_URL:latest
