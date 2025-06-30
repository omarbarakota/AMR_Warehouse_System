# Home Location Management API

## Overview
The Home Location Management API allows administrators to view and update the robot's home position coordinates. This home location is used in all package delivery operations.

## Authentication
All endpoints require admin-level authentication. Non-admin users will receive a 403 Forbidden response.

## Endpoints

### 1. Get Current Home Location
**GET** `/api/admin/home-location`

Returns the current home location coordinates.

**Response:**
```json
{
  "status": "success",
  "data": {
    "x_coordinate": 1.5,
    "y_coordinate": 2.0,
    "theta_coordinate": 0.785,
    "updated_at": "2025-06-29T15:24:36.506356"
  }
}
```

### 2. Update Home Location
**PUT** `/api/admin/home-location`

Updates the home location coordinates.

**Request Body:**
```json
{
  "x_coordinate": 1.5,
  "y_coordinate": 2.0,
  "theta_coordinate": 0.785
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Home location updated successfully",
  "data": {
    "x_coordinate": 1.5,
    "y_coordinate": 2.0,
    "theta_coordinate": 0.785,
    "updated_at": "2025-06-29T15:24:36.506356"
  }
}
```

## Usage Examples

### Using curl

**Get current home location:**
```bash
curl -X GET http://localhost:5000/api/admin/home-location \
  -H "Cookie: session=your_session_cookie"
```

**Update home location:**
```bash
curl -X PUT http://localhost:5000/api/admin/home-location \
  -H "Content-Type: application/json" \
  -H "Cookie: session=your_session_cookie" \
  -d '{
    "x_coordinate": 1.5,
    "y_coordinate": 2.0,
    "theta_coordinate": 0.785
  }'
```

### Using JavaScript

**Get current home location:**
```javascript
fetch('/api/admin/home-location', {
  method: 'GET',
  credentials: 'include'
})
.then(response => response.json())
.then(data => {
  console.log('Current home location:', data.data);
});
```

**Update home location:**
```javascript
fetch('/api/admin/home-location', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json'
  },
  credentials: 'include',
  body: JSON.stringify({
    x_coordinate: 1.5,
    y_coordinate: 2.0,
    theta_coordinate: 0.785
  })
})
.then(response => response.json())
.then(data => {
  console.log('Home location updated:', data.message);
});
```

## Impact on Package Delivery

When you update the home location, all subsequent package deliveries will use the new coordinates in the "home" section of the MQTT message:

```json
{
  "target": {
    "x": 5.0,
    "y": 3.0,
    "theta": 1.57,
    "level": 2
  },
  "home": {
    "x": 1.5,
    "y": 2.0,
    "theta": 0.785
  }
}
```

## Console Logging

All home location operations are logged to the console with detailed information:

```
🏠 Home Location Update Request:
   New Coordinates: x=1.5, y=2.0, theta=0.785
   Updated by: admin
✅ Home location updated successfully
💾 Database: Home location stored
```

## Error Handling

- **403 Forbidden**: User is not an admin
- **400 Bad Request**: Invalid data format
- **404 Not Found**: Home location not found (for GET requests)

## Database Schema

The home location is stored in the `home_location` table:

```sql
CREATE TABLE home_location (
    id INTEGER PRIMARY KEY,
    x_coordinate FLOAT NOT NULL DEFAULT 0.0,
    y_coordinate FLOAT NOT NULL DEFAULT 0.0,
    theta_coordinate FLOAT NOT NULL DEFAULT 0.0,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by INTEGER REFERENCES user(id)
);
``` 