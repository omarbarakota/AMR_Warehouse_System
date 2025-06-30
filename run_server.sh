#!/usr/bin/env bash

# Auto-detect the first non-loopback IPv4 address
DEVICE_IP=$(hostname -I | awk '{print $1}')

echo "Detected device IP: $DEVICE_IP"
echo "Starting Gunicorn on ${DEVICE_IP}:8000 ..."

# Run Gunicorn, binding to your device's IP on port 8000
gunicorn wsgi --bind ${DEVICE_IP}:8000 