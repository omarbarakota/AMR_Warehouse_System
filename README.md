Certainly. Below is your **fully updated and corrected `README.md`** file with all relevant modifications:

---

# AMR Control & Monitoring Web Application

[![Testing and CI / CD](https://github.com/omarbarakota/AMR_Warehouse_System/actions/workflows/image_update.yaml/badge.svg)](https://github.com/omarbarakota/AMR_Warehouse_System/actions/workflows/image_update.yaml)

## Table of Contents

- [AMR Control \& Monitoring Web Application](#amr-control--monitoring-web-application)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Project Description](#project-description)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Folder Structure](#folder-structure)
  - [Best Practices](#best-practices)
  - [Additional Notes](#additional-notes)
  - [Features](#features)
  - [Quick Start: Deploying on Another Machine](#quick-start-deploying-on-another-machine)
  - [More Details](#more-details)
  - [License](#license)

---

## Introduction

This project is a modern web-based control and monitoring system for Autonomous Mobile Robots (AMRs). It provides a dashboard for real-time robot control, MQTT message logging, user and role management, command tracking, and system logs. The backend is built using Flask, SQLAlchemy for the database, and MQTT for robot communication. The frontend uses Bootstrap and JavaScript to deliver a clean and responsive UI.

## Project Description

Key capabilities include:

* **Manual & Automatic Robot Control** through an intuitive dashboard.
* **MQTT Message Logging**: Every message is saved to the database for review.
* **User Management System**: Role-based access control for Admins, Operators, and Viewers.
* **Go-To Commands**: Issue location-based commands to direct robot movement.
* **Command & Event Logs**: Track all issued commands and system actions.
* **Real-Time Monitoring**: View robot status and live updates through WebSocket.
* **Secure Web Interface**: Accessible from local or remote clients via IP and port.

---

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/omarbarakota/AMR_Warehouse_System.git
   cd AMR_Warehouse_System
   ```

2. **Create a Python virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**:

   ```bash
   python main.py
   ```

5. **Access the dashboard**:

   ```
   http://<your-server-ip>:8000
   ```

   Replace `<your-server-ip>` with the actual local IP address, e.g., `192.168.1.100`.

   * On **Windows**: Run `ipconfig`
   * On **Linux/macOS**: Run `ifconfig` or `ip a`

---

## Usage

1. **Login**: Navigate to `/login` and sign in with your credentials.
2. **Dashboard**: Control the robot, issue commands, and monitor logs.
3. **Admin Panel**:

   * Manage users and their roles.
   * Update home location.
   * View all logs and MQTT message history.
4. **Real-Time Communication**: Uses WebSocket and MQTT protocols for responsive updates.
5. **Metrics**: Available at `/metrics` for Prometheus-based monitoring.

---

## Folder Structure

```plaintext
project/
├── main.py              # Core Flask app logic
├── wsgi.py              # WSGI entry point
├── static/              # CSS, JS, fonts, images
├── templates/           # HTML (Jinja2) templates
├── tests/               # Automated testing
├── requirements.txt     # Python dependencies
└── run_server           # Launch script
```

---

## Best Practices

1. **Security**

   * Use `.env` for secrets (not hardcoded).
   * Run behind HTTPS in production.
   * Limit login attempts, sanitize inputs.

2. **Code Organization**

   * Separate concerns (routes, models, services).
   * Use Blueprints for modularity.

3. **Testing**

   * Use `pytest` for unit/integration tests.
   * Include mocking for external interfaces (MQTT, DB).

4. **Deployment**

   * Containerize with Docker.
   * Use CI/CD tools for automated testing & deployment.

---

## Additional Notes

* **SSL Setup (Optional)**: Use `mkcert` to generate self-signed SSL certificates for development.
* **Firewall Settings**: Ensure port 8000 is open if you plan to access the app over a local network.
* **Custom Hostname**: Add a mapping in `/etc/hosts` (Linux/macOS) or `C:\Windows\System32\drivers\etc\hosts` (Windows).

  ```bash
  192.168.x.x robot.local
  ```

---

## Features

* **User Authentication & RBAC**: Role-based login (admin, operator, viewer).
* **Real-Time Dashboard**: Live robot control and message feedback.
* **Admin Panel**: Manage users, view MQTT logs, track command history.
* **MQTT Integration**: Subscribes, publishes, and logs all relevant robot messages.
* **SQLite Database**: Stores users, messages, commands, logs.
* **Responsive Design**: Mobile and desktop friendly interface.
* **Extensive Tests**: For endpoints, RBAC logic, and critical flows.

---

## Quick Start: Deploying on Another Machine

1. **Clone the repo**:

   ```bash
   git clone https://github.com/omarbarakota/AMR_Warehouse_System.git
   cd AMR_Warehouse_System
   ```

2. **(Optional) Create a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**:

   ```bash
   ./run_server
   ```

   Then visit:
   `http://<your-server-ip>:8000`
   (Replace `<your-server-ip>` with the actual machine IP)

5. **Default Admin Login**:

   * Username: `admin`
   * Password: `123`

6. **(Optional) Run tests**:

   ```bash
   ./run_all_tests.sh
   ```

---

## More Details

* [static/README.md](app/static/README.md): Static file usage
* [static/js/README.md](app/static/js/README.md): JavaScript responsibilities
* [static/css/README.md](app/static/css/README.md): CSS structure
* [templates/README.md](app/templates/README.md): Jinja2 page descriptions
* [tests/README.md](app/tests/README.md): Test suite overview

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

Let me know if you'd like a [clean version formatted as a GitHub Gist](f), or [Dockerfile integration steps](f).
