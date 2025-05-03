#!/usr/bin/env bash
# Test script for mini_webserver
set -e
cd "$(dirname "$0")"

PORT=8881

# Build the server
make

# Remove old log
rm -f access.log

# Start the server in the background
./mini_webserver public_html $PORT &
SERVER_PID=$!
sleep 1

# Make a request
RESPONSE=$(curl -s http://localhost:$PORT/index.html)

# Check the response
if echo "$RESPONSE" | grep -q "Hello, World!"; then
    echo "Test passed: HTML content served."
else
    echo "Test failed: HTML content not served."
    kill $SERVER_PID
    wait $SERVER_PID 2>/dev/null || true
    exit 1
fi

# Check the access.log for the request path
if grep -q "/index.html" access.log; then
    echo "Test passed: Request path logged to access.log."
else
    echo "Test failed: Request path not logged to access.log."
    kill $SERVER_PID
    wait $SERVER_PID 2>/dev/null || true
    exit 1
fi

# Test port-in-use error handling
set +e
PORT_IN_USE_MSG=$(./mini_webserver public_html $PORT 2>&1)
set -e
if echo "$PORT_IN_USE_MSG" | grep -q "already in use"; then
    echo "Test passed: Port in use error detected."
else
    echo "Test failed: Port in use error not detected."
    kill $SERVER_PID
    wait $SERVER_PID 2>/dev/null || true
    exit 1
fi

# Kill the server
kill $SERVER_PID
wait $SERVER_PID 2>/dev/null || true
rm -f access.log 