from flask import Flask, request, jsonify
from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from flask_socketio import SocketIO, emit               # For live data updates via WebSocket
from flask_httpauth import HTTPBasicAuth                # For authentication
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import paho.mqtt.client as mqtt
from werkzeug.security import generate_password_hash, check_password_hash
import json
from functools import wraps
import os

# Initialize Flask app and extensions
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Secret key for session management

# --- Database Configuration ---
# Define the absolute path for the instance folder and database
instance_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'instance')
if not os.path.exists(instance_dir):
    os.makedirs(instance_dir)
db_path = os.path.join(instance_dir, 'app_database.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# MQTT Configuration
MQTT_BROKER = os.environ.get("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.environ.get("MQTT_PORT", 1883))
MQTT_TOPIC = "/test/topic"

# Initialize MQTT Client with the latest API version
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# --- Database Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    mqtt_messages = db.relationship('MQTTMessage', backref='user', lazy=True)
    system_logs = db.relationship('SystemLog', backref='user', lazy=True)

class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    x_coordinate = db.Column(db.Float, nullable=False)
    y_coordinate = db.Column(db.Float, nullable=False)
    theta_coordinate = db.Column(db.Float, nullable=False)
    level = db.Column(db.String(10), default='level1')
    location_description = db.Column(db.String(200), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MQTTMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    message_type = db.Column(db.String(20), default='received')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

class SystemLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)

class HomeLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x_coordinate = db.Column(db.Float, default=0.0, nullable=False)
    y_coordinate = db.Column(db.Float, default=0.0, nullable=False)
    theta_coordinate = db.Column(db.Float, default=0.0, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

# --- MQTT Handlers ---
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"❌ Failed to connect to MQTT Broker: {reason_code}")
        return
    # Subscribe to all relevant topics
    client.subscribe("/test/topic")
    client.subscribe("/robot/goal")
    client.subscribe("/robot/grippermove")
    client.subscribe("/robot/lift")
    client.subscribe("/robot/emergency")
    client.subscribe("/robot/move")
    client.subscribe("/amr/delivery/#")
    print(f"[INFO] Connected to MQTT Broker at {MQTT_BROKER}:{MQTT_PORT}")
    print(f"Connected to MQTT broker with result code {reason_code}")
    # Log connection to database
    try:
        with app.app_context():
            log_entry = SystemLog(
                level='INFO',
                message=f'Connected to MQTT broker with result code {reason_code}',
                ip_address='system'
            )
            db.session.add(log_entry)
            db.session.commit()
    except Exception as e:
        pass  # Silently ignore database errors

def on_message(client, userdata, msg):
    try:
        with app.app_context():
            mqtt_message = MQTTMessage(topic=msg.topic, message=msg.payload.decode(), message_type='received')
            db.session.add(mqtt_message)
            db.session.commit()
    except Exception as e:
        pass # Ignore db errors

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

try:
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
except Exception as e:
    print(f"❌ MQTT Connection Failed: {e}")

mqtt_client.loop_start()

# --- Database Initialization ---
def init_database():
    with app.app_context():
        db.create_all()
        
        if User.query.filter_by(username='admin').first() is None:
            admin_user = User(username='admin', password_hash=generate_password_hash('123'), email='admin@example.com', role='admin')
            db.session.add(admin_user)
        
        default_users = [
            {'username': 'viewer', 'password': 'viewer123', 'email': 'viewer@example.com', 'role': 'viewer'},
            {'username': 'user', 'password': 'user123', 'email': 'user@example.com', 'role': 'user'},
            {'username': 'operator', 'password': 'operator123', 'email': 'operator@example.com', 'role': 'operator'},
        ]
        
        for user_data in default_users:
            if User.query.filter_by(username=user_data['username']).first() is None:
                new_user = User(username=user_data['username'], password_hash=generate_password_hash(user_data['password']), email=user_data['email'], role=user_data['role'])
                db.session.add(new_user)
        
        if Package.query.count() == 0:
            sample_packages = [
                Package(package_id='PKG001', name='Package 1', x_coordinate=5.26, y_coordinate=-1.01, theta_coordinate=-2.29, level='level1'),
                Package(package_id='PKG002', name='Package 2', x_coordinate=3.5, y_coordinate=2.0, theta_coordinate=1.57, level='level2'),
                Package(package_id='PKG003', name='Package 3', x_coordinate=1.91, y_coordinate=-0.36, theta_coordinate=2.81, level='level3'),
                Package(package_id='PKG004', name='Package 4', x_coordinate=2.51, y_coordinate=-0.06, theta_coordinate=3.81, level='level2'),
                Package(package_id='PKG005', name='Package 5', x_coordinate=2.91, y_coordinate=-3.36, theta_coordinate=2.51, level='level1'),
                Package(package_id='HOME', name='Home Base', x_coordinate=0.0, y_coordinate=0.0, theta_coordinate=0.0, level='level1')
            ]
            db.session.bulk_save_objects(sample_packages)
        
        if HomeLocation.query.first() is None:
            home_location = HomeLocation(x_coordinate=0.0, y_coordinate=0.0, theta_coordinate=0.0)
            db.session.add(home_location)
            
        db.session.commit()

# --- Utility and Helper Functions ---
def role_required(allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not session.get("logged_in") or session.get("role") not in allowed_roles:
                return jsonify({"status": "error", "message": "Forbidden"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator

def convert_to_float(data):
    if isinstance(data, dict):
        return {k: convert_to_float(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_float(elem) for elem in data]
    elif isinstance(data, (int, float)):
        return float(data)
    else:
        return data

def get_home_location():
    home = HomeLocation.query.first()
    if home:
        return {'x': home.x_coordinate, 'y': home.y_coordinate, 'theta': home.theta_coordinate}
    return {'x': 0.0, 'y': 0.0, 'theta': 0.0}

def convert_level_to_numeric(level):
    return {'level1': 1, 'level2': 2, 'level3': 3}.get(level, 1)

# --- Routes ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session["logged_in"] = True
            session["username"] = username
            session["role"] = user.role
            user.last_login = datetime.utcnow()
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@role_required(['viewer','user', 'operator', 'admin'])
def index():
    # Determine if the user has control permissions
    can_control = session.get("role") in ['user','operator', 'admin']
    return render_template('index.html', username=session.get("username"), role=session.get("role"), can_control=can_control)

@app.route('/database')
@role_required(['operator', 'admin'])
def database_view():
    users = User.query.all()
    packages = Package.query.all()
    mqtt_messages = MQTTMessage.query.all()
    system_logs = SystemLog.query.all()
    return render_template('database.html', users=users, packages=packages, mqtt_messages=mqtt_messages, system_logs=system_logs)

@app.route('/admin')
@role_required(['admin'])
def admin():
    users = User.query.all()
    packages = Package.query.all()
    mqtt_messages = MQTTMessage.query.all()
    system_logs = SystemLog.query.all()
    return render_template(
        'admin.html',
        users=users,
        packages=packages,
        mqtt_messages=mqtt_messages,
        system_logs=system_logs
    )

@app.route('/users')
@role_required(['admin'])
def users_view():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/api/users', methods=['GET'])
@role_required(['admin'])
def api_get_users():
    users = User.query.all()
    return jsonify([
        {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'last_login': user.last_login.isoformat() if user.last_login else None
        }
        for user in users
    ])
@app.route('/api/users', methods=['POST'])
@role_required(['admin'])
def api_create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')
    email = data.get('email')

    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Username and password are required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'status': 'error', 'message': 'Username already exists'}), 400

    new_user = User(
        username=username,
        password_hash=generate_password_hash(password),
        email=email,
        role=role
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'User created successfully'})

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@role_required(['admin'])
def api_delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    if user.role == 'admin':
        return jsonify({'status': 'error', 'message': 'Cannot delete admin user'}), 403
    db.session.delete(user)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'User deleted successfully'})
@app.route('/api/packages', methods=['POST'])
@role_required(['admin'])
def api_add_package():
    data = request.json
    try:
        new_package = Package(
            package_id=data['package_id'],
            name=data['name'],
            x_coordinate=float(data['x_coordinate']),
            y_coordinate=float(data['y_coordinate']),
            theta_coordinate=float(data['theta_coordinate']),
            level=data.get('level', 'level1')
        )
        db.session.add(new_package)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Package added successfully'}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/packages')
@role_required(['user', 'operator', 'admin'])
def api_packages():
    packages = Package.query.filter_by(is_active=True).all()
    package_list = [{'id': p.id, 'package_id': p.package_id, 'name': p.name, 'x': p.x_coordinate, 'y': p.y_coordinate, 'theta': p.theta_coordinate, 'level': p.level} for p in packages]
    return jsonify(package_list)

@app.route('/deliver_package', methods=['POST'])
@role_required(['user', 'operator', 'admin'])
def deliver_package():
    data = request.json
    package_id = data.get('package_id')
    pkg = Package.query.filter_by(package_id=package_id).first()
    if not pkg:
        return jsonify({'status': 'error', 'message': 'Package not found'}), 404

    home_location = get_home_location()
    mqtt_message = {
        "target": {"x": pkg.x_coordinate, "y": pkg.y_coordinate, "theta": pkg.theta_coordinate, "level": convert_level_to_numeric(pkg.level)},
        "home": home_location
    }
    
    mqtt_message = convert_to_float(mqtt_message)
    topic = f"/amr/delivery/{package_id}"
    
    print(f"📡 Topic: {topic}")
    print(f"📦 Data: {json.dumps(mqtt_message, indent=2)}")
    
    mqtt_client.publish(topic, json.dumps(mqtt_message))
    
    return jsonify(mqtt_message)

@app.route('/api/packages/<int:package_id>/toggle-active', methods=['PUT'])
@role_required(['admin'])
def toggle_package_active(package_id):
    pkg = Package.query.get(package_id)
    if not pkg:
        return jsonify({'status': 'error', 'message': 'Package not found'}), 404
    data = request.get_json()
    pkg.is_active = data.get('is_active', True)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Package status updated.'})

@app.route('/publish', methods=['POST'])
@role_required(['user', 'operator', 'admin'])
def publish_message():
    data = request.json
    topic = data.get("topic", MQTT_TOPIC)
    message = data.get("message", "default message")

    processed_message = message
    try:
        message_data = json.loads(message)
        if topic == "/amr/joystick" and "z" in message_data:
            if isinstance(message_data.get("z"), (int, float)):
                message_data["z"] = -message_data["z"]
        
        if topic == "/amr/operation/home" and message_data.get("operation") == "return_home":
            home_location = get_home_location()
            message_data["coordinates"] = home_location
            
        message_data = convert_to_float(message_data)
        processed_message = json.dumps(message_data)
    except (json.JSONDecodeError, TypeError):
        pass
    
    print(f"📡 Topic: {topic}")
    print(f"📦 Data: {processed_message}")
    
    mqtt_client.publish(topic, processed_message)
    
    # Log published message
    try:
        user_id = session.get('user_id')
        db.session.add(MQTTMessage(topic=topic, message=processed_message, message_type='published', user_id=user_id))
        db.session.commit()
    except Exception as e:
        print(f"Failed to log published MQTT message: {e}")

    return jsonify({"status": "Message published", "topic": topic, "message": processed_message})

@app.route('/api/admin/home-location', methods=['PUT'])
@role_required(['admin'])
def api_update_home_location():
    data = request.json
    home = HomeLocation.query.first()
    if not home:
        home = HomeLocation()
        db.session.add(home)
    
    home.x_coordinate = data.get('x_coordinate', home.x_coordinate)
    home.y_coordinate = data.get('y_coordinate', home.y_coordinate)
    home.theta_coordinate = data.get('theta_coordinate', home.theta_coordinate)
    home.updated_by = User.query.filter_by(username=session["username"]).first().id
    
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Home location updated'})

@app.route('/api/admin/delete-mqtt-messages', methods=['DELETE'])
@role_required(['admin'])
def delete_mqtt_messages():
    MQTTMessage.query.delete()
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'All MQTT messages deleted.'})

@app.route('/api/admin/delete-system-logs', methods=['DELETE'])
@role_required(['admin'])
def delete_system_logs():
    SystemLog.query.delete()
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'All system logs deleted.'})

@app.route('/api/admin/delete-old-data', methods=['DELETE'])
@role_required(['admin'])
def delete_old_data():
    from datetime import datetime, timedelta
    data = request.get_json()
    days = data.get('days', 7)
    cutoff = datetime.utcnow() - timedelta(days=days)
    deleted_mqtt = MQTTMessage.query.filter(MQTTMessage.timestamp < cutoff).delete()
    deleted_logs = SystemLog.query.filter(SystemLog.timestamp < cutoff).delete()
    db.session.commit()
    return jsonify({'status': 'success', 'message': f'Deleted {deleted_mqtt} MQTT messages and {deleted_logs} logs older than {days} days.'})

@app.route('/api/packages/<int:package_id>', methods=['GET'])
@role_required(['admin'])
def get_package(package_id):
    pkg = Package.query.get(package_id)
    if not pkg:
        return jsonify({'status': 'error', 'message': 'Package not found'}), 404
    return jsonify({
        'id': pkg.id,
        'package_id': pkg.package_id,
        'name': pkg.name,
        'x_coordinate': pkg.x_coordinate,
        'y_coordinate': pkg.y_coordinate,
        'theta_coordinate': pkg.theta_coordinate,
        'level': pkg.level,
        'location_description': pkg.location_description,
        'is_active': pkg.is_active
    })

@app.route('/api/packages/<int:package_id>', methods=['PUT'])
@role_required(['admin'])
def update_package(package_id):
    pkg = Package.query.get(package_id)
    if not pkg:
        return jsonify({'status': 'error', 'message': 'Package not found'}), 404
    data = request.get_json()
    pkg.package_id = data.get('package_id', pkg.package_id)
    pkg.name = data.get('name', pkg.name)
    pkg.x_coordinate = data.get('x_coordinate', pkg.x_coordinate)
    pkg.y_coordinate = data.get('y_coordinate', pkg.y_coordinate)
    pkg.theta_coordinate = data.get('theta_coordinate', pkg.theta_coordinate)
    pkg.level = data.get('level', pkg.level)
    pkg.location_description = data.get('location_description', pkg.location_description)
    pkg.is_active = data.get('is_active', pkg.is_active)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Package updated successfully'})

@app.route('/api/packages/<int:package_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_package(package_id):
    pkg = Package.query.get(package_id)
    if not pkg:
        return jsonify({'status': 'error', 'message': 'Package not found'}), 404
    db.session.delete(pkg)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Package deleted successfully'})

@app.route('/api/home-location', methods=['GET'])
def api_get_home_location():
    home = HomeLocation.query.first()
    if home:
        return jsonify({
            'x': home.x_coordinate,
            'y': home.y_coordinate,
            'theta': home.theta_coordinate,
            'level': getattr(home, 'level', 1)  # fallback if level not present
        })
    return jsonify({'x': 0.0, 'y': 0.0, 'theta': 0.0, 'level': 1})

@app.route('/api/mqtt-messages', methods=['GET'])
def api_get_mqtt_messages():
    msg_type = request.args.get('type', 'all')
    query = MQTTMessage.query
    if msg_type == 'published':
        query = query.filter_by(message_type='published')
    elif msg_type == 'received':
        query = query.filter_by(message_type='received')
    messages = query.order_by(MQTTMessage.timestamp.desc()).all()
    return jsonify([
        {
            'id': m.id,
            'topic': m.topic,
            'message': m.message,
            'message_type': m.message_type,
            'user': m.user.username if m.user else None,
            'timestamp': m.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        } for m in messages
    ])

# Initialize database within the app context when the app starts
with app.app_context():
    init_database()
