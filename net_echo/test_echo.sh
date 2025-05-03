#!/usr/bin/env bash

# Test script for net_echo server and client
set -e
PORT=54321
MESSAGE="hello_test"

# Start server in background
./server $PORT &
SERVER_PID=$!
sleep 1  # Give server time to start

# Run client and capture output
OUTPUT=$(./client 127.0.0.1 $PORT "$MESSAGE")

# Kill server
kill $SERVER_PID
wait $SERVER_PID 2>/dev/null || true

# Check output
if echo "$OUTPUT" | grep -q "$MESSAGE"; then
    echo "Test passed: Echoed message received."
else
    echo "Test failed: Echoed message not received."
    exit 1
fi 