#!/usr/bin/env sh
# Test server connectivity
set -euo pipefail

# start the container
echo "starting container with test server..."
docker rm -f test-server > /dev/null 2>&1 || true
docker compose run -itd --build --service-ports --name test-server bot
echo

# wait for the server to start
echo "waiting for server to start..."
sleep 5

# load connection settings
# shellcheck source=/dev/null
[ -f .env ] && . .env
url="http://localhost:${SERVER_PORT:-8081}"
echo "testing connection to url: $url"

# test the connection
curl -s "$url/health"
echo && echo

# cleanup
echo "container logs:"
docker logs test-server
docker rm -f test-server > /dev/null
