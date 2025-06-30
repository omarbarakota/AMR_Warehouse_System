# Image Assets in AMR Control & Monitoring Web Application

This directory contains image assets used throughout the dashboard, map, and UI.

## File Overview

- **robot.png**: Icon or illustration of the robot, used in the dashboard or map.
- **map.png**: Map background or placeholder for the interactive map.

## Usage

- Images are referenced in HTML templates using:
  
  ```html
  <img src="{{ url_for('static', filename='img/robot.png') }}" alt="Robot">
  ```

- Images are used for UI decoration, map overlays, and branding.

---

For more details on static assets, see [../README.md](../README.md).
