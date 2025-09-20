#!/bin/sh
# Deploy bot container
set -e  # exit on any error

IMAGE_URL="ghcr.io/mohdfareed/telegram-trader"
tag="$(uv version --short)"
echo "deploying version: $tag"

# build image
echo "building image..."
docker-compose pull
docker build -t $IMAGE_URL:"${tag}" . --no-cache

# deploy image to registry
echo "pushing image to github..."
docker push $IMAGE_URL:"${tag}"

# tag and push latest if not already latest
echo "tagging build as latest..."
docker tag $IMAGE_URL:"${tag}" $IMAGE_URL:latest
docker push $IMAGE_URL:latest
