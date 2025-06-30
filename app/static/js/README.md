# JavaScript Files in AMR Control & Monitoring Web Application

This directory contains all JavaScript files used for frontend interactivity, dashboard logic, MQTT/WebSocket communication, and UI enhancements.

## File Overview

- **dashboard.js**: Main dashboard logic for robot control, package management, home position, and MQTT goal publishing.
- **manual.js**: Handles manual robot movement controls (e.g., arrow buttons, joystick).
- **funcs.js**: Utility functions for MQTT publishing, topic subscription, and UI helpers.
- **client.js**: MQTT client connection setup for browser-based MQTT.js usage.
- **map.js**: Handles map rendering, robot pose drawing, and map image updates.
- **topics.js**: Defines MQTT topics to subscribe to for live monitoring.
- **main.js**: General app initialization, MQTT connection, and event handlers.
- **mqtt.min.js**: Minified MQTT.js library for browser MQTT communication.
- **socket.io.min.js**: Minified Socket.IO library for real-time WebSocket communication.
- **leaflet.js**: Minified Leaflet.js library for interactive maps.
- **jquery.min.js**: Minified jQuery library (if used by any UI components).
- **bootstrap.bundle.min.js**: Minified Bootstrap JS for UI components.
- **monitoring.js**: Handles live monitoring dashboard logic and MQTT topic updates.
- **topics_data.js**: Handles dynamic topic data display in the monitoring dashboard.
- **elements.js**: DOM element references and helpers for monitoring and dashboard pages.

## Usage

- All files are loaded via `<script>` tags in the relevant HTML templates.
- Most files are modular and only loaded where needed (e.g., `dashboard.js` for the main dashboard, `manual.js` for manual control, etc.).
- Vendor libraries (minified) are only updated via package manager or official sources.

---

For more details on static assets, see [../README.md](../README.md).
