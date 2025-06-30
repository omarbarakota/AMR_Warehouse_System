# Role-Based Access Control System

## Overview

The AMR Control System now implements a comprehensive role-based access control (RBAC) system with four distinct user types, each with specific permissions and capabilities.

## User Roles

### 1. Viewer 👁️
**Username:** `viewer` | **Password:** `viewer123`

**Permissions:**
- ✅ View robot position on the map
- ✅ Monitor battery percentage
- ✅ View connection status
- ✅ View current task status
- ✅ Access the main dashboard

**Restrictions:**
- ❌ Cannot control robot movement
- ❌ Cannot access sensor data
- ❌ Cannot view MQTT messages
- ❌ Cannot access database views
- ❌ Cannot manage users or system

**Use Case:** Perfect for supervisors, visitors, or anyone who needs to monitor the robot's status without control capabilities.

---

### 2. User 🎮
**Username:** `user` | **Password:** `user123`

**Permissions:**
- ✅ All viewer permissions
- ✅ Control robot movement (up, down, left, right, stop)
- ✅ Send robot to specific packages
- ✅ Return robot to home position
- ✅ Access manual control interface

**Restrictions:**
- ❌ Cannot view sensor data
- ❌ Cannot view MQTT messages
- ❌ Cannot access database views
- ❌ Cannot manage users or system

**Use Case:** Ideal for operators who need to control the robot's movement and navigation but don't need access to system data.

---

### 3. Operator 🔧
**Username:** `operator` | **Password:** `operator123`

**Permissions:**
- ✅ All user permissions
- ✅ View sensor data and readings
- ✅ View MQTT messages
- ✅ Access database view (read-only)
- ✅ Add sensor data
- ✅ Access monitoring interface

**Restrictions:**
- ❌ Cannot manage database content
- ❌ Cannot create/edit/delete users
- ❌ Cannot access admin functions

**Use Case:** Perfect for technical operators who need to monitor system health, view sensor data, and control the robot.

---

### 4. Admin 🔐
**Username:** `admin` | **Password:** `123`

**Permissions:**
- ✅ All operator permissions
- ✅ Full database management
- ✅ Create, edit, and delete users (except other admins)
- ✅ Manage packages (add, edit, delete)
- ✅ Delete system logs, MQTT messages, and sensor data
- ✅ Access admin interface
- ✅ Full system control

**Restrictions:**
- ❌ Cannot edit or delete other admin users (protected)

**Use Case:** System administrators who need complete control over the system, user management, and database operations.

---

## Access Control Implementation

### Route Protection

The system uses decorators to protect routes based on user roles:

```python
@role_required(['admin'])           # Admin only
@role_required(['operator', 'admin'])  # Operator and Admin
@role_required(['user', 'operator', 'admin'])  # User, Operator, and Admin
```

### Permission Functions

The system includes helper functions to check permissions:

```python
can_view_robot()      # All roles
can_control_robot()   # User, Operator, Admin
can_view_sensors()    # Operator, Admin
can_view_messages()   # Operator, Admin
can_manage_database() # Admin only
can_manage_users()    # Admin only
```

### Template-Level Access Control

The frontend templates conditionally show/hide elements based on user role:

```html
{% if role in ['operator', 'admin'] %}
  <!-- Show monitoring and database links -->
{% endif %}

{% if role == 'admin' %}
  <!-- Show admin link -->
{% endif %}

{% if can_control %}
  <!-- Show robot controls -->
{% else %}
  <!-- Show viewer-only message -->
{% endif %}
```

## User Management

### Creating Users

Admins can create new users through the User Management interface (`/users`):

1. **Username:** Unique identifier
2. **Email:** Optional contact information
3. **Password:** Secure password
4. **Role:** One of viewer, user, or operator

### Editing Users

Admins can edit user information:
- Change email address
- Update password
- Modify role (except admin users)
- Cannot edit other admin users

### Deleting Users

Admins can delete users:
- Cannot delete admin users (protected)
- Deletion is permanent and cannot be undone

## Security Features

### Session Management
- Secure session handling with Flask sessions
- Automatic logout on session expiration
- Role information stored in session

### Password Security
- Passwords are hashed using Werkzeug's `generate_password_hash`
- Secure password verification with `check_password_hash`

### Access Logging
- All user actions are logged to the system log
- Failed login attempts are tracked
- User activity is recorded with IP addresses

## Default Users

The system automatically creates these default users:

| Username | Password | Role | Description |
|----------|----------|------|-------------|
| `admin` | `123` | Admin | Full system administrator |
| `viewer` | `viewer123` | Viewer | Read-only access |
| `user` | `user123` | User | Basic robot control |
| `operator` | `operator123` | Operator | Advanced monitoring and control |

## API Endpoints by Role

### Viewer
- `GET /` - Dashboard (view-only)

### User
- `GET /` - Dashboard with controls
- `GET /manual` - Manual control interface
- `GET /api/packages` - Active packages
- `POST /publish` - Publish MQTT messages

### Operator
- All User endpoints
- `GET /data` - Monitoring interface
- `GET /database` - Database view
- `GET /api/mqtt-messages` - MQTT messages
- `GET /api/system-logs` - System logs
- `GET /api/sensor-data` - Sensor data
- `GET /api/packages/all` - All packages
- `POST /api/add-sensor-data` - Add sensor data
- `GET /receive` - Receive MQTT messages

### Admin
- All Operator endpoints
- `GET /admin` - Admin interface
- `GET /users` - User management
- `GET /api/users` - User list
- `POST /api/users` - Create user
- `PUT /api/users/<id>` - Update user
- `DELETE /api/users/<id>` - Delete user
- `POST /api/packages` - Create package
- `PUT /api/packages/<id>` - Update package
- `DELETE /api/packages/<id>` - Delete package
- `DELETE /api/admin/delete-*` - Delete data

## Getting Started

1. **Start the server:**
   ```bash
   python3 app/main.py
   ```

2. **Access the application:**
   - Go to `http://localhost:5000`
   - You'll be redirected to login

3. **Login with different roles:**
   - **Admin:** `admin` / `123`
   - **Viewer:** `viewer` / `viewer123`
   - **User:** `user` / `user123`
   - **Operator:** `operator` / `operator123`

4. **Test different permissions:**
   - Try accessing different pages with different roles
   - Verify that controls are shown/hidden appropriately
   - Test API endpoints with different user types

## Best Practices

1. **Use the principle of least privilege:** Assign users the minimum role needed
2. **Regular password updates:** Encourage users to change default passwords
3. **Monitor system logs:** Check for failed login attempts and suspicious activity
4. **Backup user data:** Regularly backup the database
5. **Audit user permissions:** Periodically review user roles and permissions

## Troubleshooting

### Common Issues

1. **"Insufficient permissions" error:**
   - Check if the user has the required role
   - Verify the route protection is working correctly

2. **Cannot access admin functions:**
   - Ensure you're logged in as an admin user
   - Check if the session contains the correct role

3. **User management not working:**
   - Verify you're logged in as admin
   - Check if the user you're trying to edit is not an admin

### Debug Mode

Enable debug mode to see detailed error messages:
```python
app.run(debug=True)
```

## Future Enhancements

1. **Role hierarchy:** Implement role inheritance
2. **Custom permissions:** Allow granular permission control
3. **Two-factor authentication:** Add 2FA for admin accounts
4. **Audit trail:** Enhanced logging and reporting
5. **User groups:** Group-based permission management 