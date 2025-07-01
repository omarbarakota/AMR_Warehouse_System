#!/usr/bin/env bash

DEVICE_IP=${DEVICE_IP:-127.0.0.1}
PORT=8000

echo "Detected device IP: $DEVICE_IP"
echo "Starting Gunicorn on ${DEVICE_IP}:${PORT} ..."

# Run Gunicorn, binding to your device's IP on port 8000
gunicorn wsgi:application --bind ${DEVICE_IP}:8000 &
sleep 5
GUNICORN_PID=$!


./run_all_tests.sh



# If tests succeed
echo "Tests passed. Stopping server..."
kill $GUNICORN_PID
