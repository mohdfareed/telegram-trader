#!/bin/bash
set -e

# shellcheck source=/dev/null
source .env

WEBHOOK_URL="http://localhost"
WEBHOOK_PORT=12000

# start the container
echo "starting container with test server..."
docker rm -f test-server > /dev/null 2>&1 || true
docker compose -p test-server run -itd --build --name test-server telegram-trader app test-server

# wait for the server to start
echo "testing connection..."
sleep 10

# test the connection
if curl -s "http://${WEBHOOK_URL}:${WEBHOOK_PORT}/" && curl -s -X POST "http://${WEBHOOK_URL}:${WEBHOOK_PORT}/test" -d "hello-world"; then
    echo "port test successful"
else
    echo "port test failed"
fi

# cleanup
echo "container logs:"
docker logs test-server
echo "cleaning up..."
docker compose -p test-server down --remove-orphans
