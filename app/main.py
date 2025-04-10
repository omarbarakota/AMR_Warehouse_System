from flask import Flask, request, jsonify
from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from flask_socketio import SocketIO, emit               # For live data updates via WebSocket
from flask_httpauth import HTTPBasicAuth                # For authentication
import paho.mqtt.client as mqtt
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app and extensions
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Secret key for session management

# MQTT Configuration
import os
# To handle the broker address in docker and pytest
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
#MQTT_BROKER = "host.docker.internal"  # Replace with your broker's address
MQTT_PORT = 1883
MQTT_TOPIC = "test/topic"

# Initialize MQTT Client
mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic: {msg.topic}")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

# User credentials (username: password)
users = {
    "admin": generate_password_hash("123")
}

# --- Utility Functions ---

def login_required(func):
    """
    Middleware to ensure the user is logged in.
    """
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# --- Routes ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page for authentication.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/logout')
def logout():
    """
    Logout route to clear session.
    """
    session.clear()
    return redirect(url_for('login'))

# Flask Routes
@app.route('/')
def index():
    """
    Index route for the dashboard.
    """
    if 'username' not in session:  # Check if user is logged in
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/data')
def get_data():
    """
    API endpoint to get the robot's current data.
    """
    if 'username' not in session:  # Check if user is logged in
        return redirect(url_for('login'))
    return render_template('monitoring.html')

@app.route('/manual')
def manual_move():
    """
    API endpoint to get the robot's current data.
    """
    if 'username' not in session:  # Check if user is logged in
        return redirect(url_for('login'))
    return render_template('manual.html')


@app.route('/publish', methods=['POST'])
def publish_message():
    if 'username' not in session:  # Check if user is logged in
        return redirect(url_for('login'))
    data = request.json
    topic = data.get("topic", MQTT_TOPIC)
    message = data.get("message", "default message")
    mqtt_client.publish(topic, message)
    return jsonify({"status": "Message published", "topic": topic, "message": message})

@app.route('/receive', methods=['GET'])
def receive_message():
    if 'username' not in session:  # Check if user is logged in
        return redirect(url_for('login'))
    return jsonify({"status": "Receiving via MQTT. Check logs for messages."})

if __name__ == '__main__':
    app.run(debug=True)
