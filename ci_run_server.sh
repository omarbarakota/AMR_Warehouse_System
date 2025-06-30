#!/usr/bin/env bash

DEVICE_IP=${DEVICE_IP:-127.0.0.1}
PORT=8000

echo "Detected device IP: $DEVICE_IP"
echo "Starting Gunicorn on ${DEVICE_IP}:${PORT} ..."

# Run Gunicorn, binding to your device's IP on port 8000
gunicorn wsgi --bind ${DEVICE_IP}:8000 


GUNICORN_PID=$!

# Wait for the server to fully start
sleep 5

# If tests succeed
echo "Tests passed. Stopping server..."
kill $GUNICORN_PID
