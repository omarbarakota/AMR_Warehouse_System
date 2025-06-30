# Database Integration Guide

This guide explains how to integrate a database with your Flask backend and display the data on the frontend. This is a complete example that you can use to learn database integration patterns.

## 🗄️ Database Overview

The application uses **SQLite** with **SQLAlchemy ORM** for database management. The database includes four main tables:

### 1. User Table
- **Purpose**: Store user accounts and authentication data
- **Fields**: id, username, password_hash, email, role, created_at, last_login
- **Relationships**: One-to-many with MQTTMessage and SystemLog

### 2. MQTTMessage Table
- **Purpose**: Store all MQTT messages (sent and received)
- **Fields**: id, topic, message, timestamp, message_type, user_id
- **Relationships**: Many-to-one with User

### 3. SystemLog Table
- **Purpose**: Store system events and user activities
- **Fields**: id, level, message, timestamp, user_id, ip_address
- **Relationships**: Many-to-one with User

### 4. SensorData Table
- **Purpose**: Store sensor readings and environmental data
- **Fields**: id, sensor_name, value, unit, timestamp, location
- **Relationships**: None (standalone data)

## 🔧 Backend Integration (Flask + SQLAlchemy)

### 1. Database Configuration
```python
# In app/main.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
```

### 2. Database Models
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    # ... other fields
```

### 3. Database Operations
```python
# Query data
users = User.query.all()
user = User.query.filter_by(username='admin').first()

# Insert data
new_user = User(username='john', password_hash='hash')
db.session.add(new_user)
db.session.commit()

# Update data
user.last_login = datetime.utcnow()
db.session.commit()

# Delete data
db.session.delete(user)
db.session.commit()
```

### 4. API Endpoints
```python
@app.route('/api/users')
@login_required
def api_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        # ... other fields
    } for user in users])
```

### 5. Template Rendering
```python
@app.route('/database')
@login_required
def database_view():
    users_data = User.query.all()
    mqtt_messages = MQTTMessage.query.order_by(MQTTMessage.timestamp.desc()).limit(50).all()
    # ... other queries
    
    return render_template('database.html', 
                         users=users_data,
                         mqtt_messages=mqtt_messages)
```

## 🎨 Frontend Integration

### 1. Server-Side Rendering (Jinja2)
```html
<!-- Display data in HTML tables -->
{% for user in users %}
<tr>
    <td>{{ user.id }}</td>
    <td>{{ user.username }}</td>
    <td>{{ user.email or 'N/A' }}</td>
    <td><span class="badge badge-{{ user.role }}">{{ user.role }}</span></td>
</tr>
{% endfor %}
```

### 2. JavaScript API Calls
```javascript
// Fetch data from API endpoints
async function fetchUsers() {
    const response = await fetch('/api/users');
    const users = await response.json();
    // Update UI with data
}

// Add new data
async function addSensorData(data) {
    const response = await fetch('/api/add-sensor-data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    const result = await response.json();
}
```

### 3. Real-time Updates
```javascript
// Auto-refresh data every 30 seconds
setInterval(refreshData, 30000);

// WebSocket integration (if needed)
socket.on('new_data', function(data) {
    // Update UI with new data
});
```

## 🚀 Getting Started

### 1. Initialize the Database
```bash
# Run the initialization script
python init_db.py
```

### 2. Start the Application
```bash
# Run your Flask application
python app/main.py
```

### 3. Access the Database Viewer
- Navigate to: `http://localhost:5000/database`
- Login with: `admin` / `123`

## 📊 Database Viewer Features

### Overview Tab
- **Statistics Cards**: Show total counts for each table
- **Learning Section**: Explains how the integration works

### Users Tab
- **User Management**: Display all users with their details
- **Role-based Badges**: Visual indicators for user roles
- **Timestamps**: Show when users were created and last logged in

### MQTT Messages Tab
- **Message History**: All sent and received MQTT messages
- **Message Types**: Color-coded badges for sent vs received
- **User Attribution**: Shows which user sent each message

### System Logs Tab
- **Activity Log**: All system events and user activities
- **Log Levels**: INFO, WARNING, ERROR with color coding
- **IP Tracking**: Shows IP addresses for security monitoring

### Sensor Data Tab
- **Data Display**: All sensor readings in a table format
- **Add New Data**: Form to add new sensor readings
- **Real-time Updates**: Auto-refresh every 30 seconds

## 🔍 Key Learning Points

### 1. Database Design
- **Relationships**: How to create one-to-many relationships
- **Indexing**: Primary keys and foreign keys
- **Data Types**: Choosing appropriate column types

### 2. Flask-SQLAlchemy Integration
- **Model Definition**: Creating database models
- **Session Management**: Using db.session for operations
- **Query Building**: Filtering, ordering, and limiting results

### 3. API Design
- **RESTful Endpoints**: Creating clean API routes
- **JSON Serialization**: Converting database objects to JSON
- **Error Handling**: Proper error responses

### 4. Frontend Integration
- **Template Rendering**: Using Jinja2 for server-side rendering
- **JavaScript APIs**: Fetching data from backend APIs
- **User Experience**: Creating responsive and intuitive interfaces

### 5. Security Considerations
- **Authentication**: Protecting routes with login_required
- **Input Validation**: Validating user input
- **SQL Injection Prevention**: Using ORM to prevent attacks

## 🛠️ Customization Examples

### Adding a New Table
```python
class NewTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### Creating a New API Endpoint
```python
@app.route('/api/new-table')
@login_required
def api_new_table():
    items = NewTable.query.all()
    return jsonify([{
        'id': item.id,
        'name': item.name,
        'created_at': item.created_at.isoformat()
    } for item in items])
```

### Adding a New Tab in the Viewer
```html
<!-- Add to nav-tabs -->
<button class="nav-tab" onclick="showTab('new-table')">New Table</button>

<!-- Add tab content -->
<div id="new-table" class="tab-content">
    <div class="data-section">
        <h2 class="section-title">New Table Data</h2>
        <div class="table-container">
            <table class="data-table">
                <!-- Table content -->
            </table>
        </div>
    </div>
</div>
```

## 📝 Best Practices

1. **Always use transactions**: Wrap database operations in try-catch blocks
2. **Validate input**: Check user input before storing in database
3. **Use relationships**: Leverage SQLAlchemy relationships for efficient queries
4. **Index important columns**: Add indexes for frequently queried columns
5. **Handle errors gracefully**: Provide meaningful error messages
6. **Log important events**: Track user activities and system events
7. **Use pagination**: Limit results for large datasets
8. **Cache frequently accessed data**: Use Redis or similar for caching

## 🔗 Additional Resources

- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/14/orm/tutorial.html)
- [Flask API Development](https://flask.palletsprojects.com/en/2.3.x/patterns/api/)
- [Jinja2 Template Engine](https://jinja.palletsprojects.com/)

This integration provides a complete example of how to build a database-driven web application with Flask. Use it as a reference for your own projects! 