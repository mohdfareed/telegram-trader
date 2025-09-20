#!/bin/sh
set -e  # exit on any error

# Trade Poster Bot - Deploy bot container
# This script builds the image and either deploys it locally
# or pushes to GitHub Container Registry for production

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
