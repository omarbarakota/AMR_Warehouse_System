# Robot Monitoring and Control Dashboard

[![Testing and CI / CD](https://github.com/omarbarakota/AMR_Warehouse_System/actions/workflows/image_update.yaml/badge.svg)](https://github.com/omarbarakota/AMR_Warehouse_System/actions/workflows/image_update.yaml)

## Table of Contents

- [Introduction](#introduction)
- [Project Description](#project-description)
- [Installation](#installation)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Best Practices](#best-practices)
- [Additional Notes](#additional-notes)

## Introduction

This project provides a web-based dashboard for monitoring and controlling a robot's live data, including speed, status, and package numbers, along with a real-time location viewer. The system integrates Flask, WebSockets, Leaflet.js, and Prometheus monitoring to offer a seamless and interactive experience.

## Project Description

The dashboard allows:

- Real-time robot data updates via WebSockets.
- Live location tracking using geolocation and OpenStreetMap.
- User authentication and session management.
- Easy API endpoints for data retrieval and updates.
- Prometheus metrics for monitoring the application.

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Create a Python virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the application:

   ```bash
   python main.py
   ```

5. Access the dashboard at:

   ```bash
   https://localhost:8000
   ```

### Steps to Access a Localhost Server on a Network

#### 1. **Bind the Server to Your Local IP Address**

Instead of binding the server to `localhost`, bind it to your local network IP (e.g., `192.168.x.x`). Here's how:

- Find your local IP:
  
  ```bash
  ip addr show  # Linux
  ifconfig      # macOS or older Linux
  ipconfig      # Windows
  ```

  Look for the IP in the format `192.168.x.x` or `10.x.x.x`.

#### 2. **Generate a Self-Signed SSL Certificate**

If you need HTTPS on a local network, use **mkcert** to generate a self-signed SSL certificate.

- Install mkcert:
  
  ```bash
  sudo apt install mkcert  # Linux
  brew install mkcert      # macOS
  choco install mkcert     # Windows
  ```

- Generate certificates for your local IP:
  
  ```bash
  mkcert 192.168.x.x
  ```

- You'll get two files: `192.168.x.x.pem` (certificate) and `192.168.x.x-key.pem` (key).

#### 3. **Set Up an HTTPS Server**

Use a lightweight HTTPS server like Python or Node.js.

- **With Python:**
  
```bash
gunicorn wsgi --bind 192.168.x.x:8000 --certfile 192.168.x.x.pem --keyfile 192.168.x.x-key.pem
```

#### 4. **Access the Server on Other Devices**

- On your PC: Visit `https://192.168.x.x:8000`.
- On other devices (connected to the same Wi-Fi network): Visit `https://192.168.x.x:8000`.

---

### Notes

- **Self-Signed Certificate Warning**: Devices accessing the site will show a "Not Secure" warning because the certificate is not signed by a recognized authority. You can bypass this by manually trusting the certificate on each device.
- **Firewall Rules**: Ensure that your firewall allows connections to port 8000 (or whatever port you're using).
- **Host Entry**: If you want to use a custom domain (like `robot.local`), set it in the `/etc/hosts` file (Linux/Mac) or `C:\Windows\System32\drivers\etc\hosts` (Windows):
  
  ```bash
  192.168.x.x robot.local
  ```

This way, you can develop and share an HTTPS site across your network securely.

## Usage

1. **Login:** Access the `/login` route to authenticate.
2. **Dashboard:** Monitor robot data and location from the main dashboard after logging in.
3. **API Endpoints:**
   - GET `/data` to retrieve current robot data.
   - POST `/update` to update robot data via JSON payloads.
4. **WebSocket:** Real-time updates are automatically pushed to connected clients.

## Folder Structure

```plaintext
project/
├── wsgi.py              # WSGI entry point
├── venv/                # Virtual environment
├── static/
│   ├── scripts.js       # JavaScript logic for WebSockets and Map
│   └── styles.css       # CSS for styling
├── templates/
│   ├── index.html       # Main dashboard page
│   ├── login.html       # Login page
├── main.py              # Flask application code
├── requirements.txt     # Python dependencies
```

## Best Practices

1. **Security:**

   - Use environment variables to store sensitive data like secret keys and passwords.
   - Configure HTTPS with a valid SSL certificate for secure communication.

2. **Code Organization:**

   - Follow Flask's recommended blueprint structure for larger applications.
   - Keep utility functions in separate modules for better maintainability.

3. **Testing:**

   - Use `pytest` for writing unit tests to ensure code reliability.
   - Mock external dependencies during testing.

4. **Scalability:**

   - Employ containerization tools like Docker for consistent deployments.
   - Consider horizontal scaling with tools like Kubernetes.

## Additional Notes

- **Prometheus Integration:** Metrics are available at `/metrics` for monitoring the application's performance.
- **Geolocation Permissions:** Ensure the browser has geolocation permissions enabled for accurate location tracking.
- **Dependencies:** Always keep the dependencies updated to avoid security vulnerabilities.

---

Developed by Omar Barakat. Feel free to contribute or report issues!

---
