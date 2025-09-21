#!/usr/bin/env sh
# Test server connectivity
set -euo pipefail

# start the container
echo "starting container with test server..."
docker rm -f test-server > /dev/null 2>&1 || true
docker compose run -itd --build --service-ports --name test-server bot app test-server
echo

# wait for the server to start
echo "waiting for server to start..."
sleep 5

# load connection settings
# shellcheck source=/dev/null
[ -f .env ] && . .env
url="http://localhost:${WEBHOOK_PORT}/"
echo "testing connection to url: $url"

# test the connection
if curl -s "$url" > /dev/null; then
    echo "GET test successful"
else
    echo "GET test failed"
fi
if curl -s -X POST "$url/test" -d "hello-world" > /dev/null; then
    echo "POST test successful"
else
    echo "POST test failed"
fi
echo

# cleanup
echo "container logs:"
docker logs test-server
docker rm -f test-server > /dev/null
