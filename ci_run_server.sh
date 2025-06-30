#!/usr/bin/env bash

DEVICE_IP=${DEVICE_IP:-127.0.0.1}
PORT=8000

echo "Detected device IP: $DEVICE_IP"
echo "Starting Gunicorn on ${DEVICE_IP}:${PORT} ..."

# Start Gunicorn in the background
gunicorn wsgi:app --bind ${DEVICE_IP}:${PORT} &
GUNICORN_PID=$!

# Wait for the server to fully start
sleep 5

# Run your tests (replace this with your test command)
echo "Running tests..."
curl -f http://${DEVICE_IP}:${PORT}/health || {
    echo "Server did not respond"
    kill $GUNICORN_PID
    exit 1
}

# If tests succeed
echo "Tests passed. Stopping server..."
kill $GUNICORN_PID
