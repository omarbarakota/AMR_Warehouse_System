# Templates in AMR Control & Monitoring Web Application

This directory contains all Jinja2 HTML templates for the web UI.

## File Overview

- **admin.html**: Admin dashboard for managing users, packages, home location, MQTT messages, and system logs.
- **index.html**: Main dashboard for robot control, map, and status overview.
- **login.html**: Login page for user authentication.
- **database.html**: Database management and viewing interface (for operators/admins).
- **manual.html**: Manual robot control interface (joystick/buttons).
- **monitoring.html**: Live monitoring dashboard for robot data and MQTT topics.
- **users.html**: User management interface (admin only).
- **client.html**: Minimal client page for MQTT/WebSocket testing.
- **images/**: Contains images used in templates (e.g., logos, map images, demo images).

## Usage

- Templates are rendered by Flask routes in `main.py`.
- Most templates extend a base layout and include static assets (CSS/JS) as needed.
- Images in `images/` are referenced in templates for branding, maps, and UI decoration.

---

For more details on the app structure, see the main [README.md](../../README.md).
