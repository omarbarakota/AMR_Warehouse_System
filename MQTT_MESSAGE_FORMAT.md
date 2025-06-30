# MQTT Message Format Documentation

## Overview
This document describes the MQTT message format used for robot navigation goals in the AMR Control System.

## Message Format

### Topic
- **Topic**: `/robot/goal`
- **Direction**: Published by web interface, consumed by robot navigation system

### Payload Structure
The MQTT message payload is a JSON object with the following structure:

```json
{
  "target": {
    "x": <float>,
    "y": <float>,
    "theta": <float>,
    "level": "<string>"
  },
  "home": {
    "x": <float>,
    "y": <float>,
    "theta": <float>
  }
}
```

### Field Descriptions

#### Target Object
- **x**: X coordinate of the target position (meters)
- **y**: Y coordinate of the target position (meters)
- **theta**: Orientation angle at the target position (radians)
- **level**: Height level of the target ("level1", "level2", "level3")

#### Home Object
- **x**: X coordinate of the home position (meters)
- **y**: Y coordinate of the home position (meters)
- **theta**: Orientation angle at the home position (radians)

## Examples

### Example 1: Package Navigation
When clicking on PKG002 (Storage Room, Level 2):

```json
{
  "target": {
    "x": 3.5,
    "y": 2.0,
    "theta": 1.57,
    "level": "level2"
  },
  "home": {
    "x": 0.0,
    "y": 0.0,
    "theta": 0.0
  }
}
```

### Example 2: Return Home
When clicking "Return Home" button:

```json
{
  "target": {
    "x": 0.0,
    "y": 0.0,
    "theta": 0.0
  },
  "home": {
    "x": 0.0,
    "y": 0.0,
    "theta": 0.0
  }
}
```

## Configuration

### Home Position
The home position is configurable by administrators through the database:
1. Access the admin interface: http://localhost:5000/admin
2. Navigate to the Packages section
3. Edit the "HOME" package coordinates
4. Save changes

### Package Levels
- **Level 1**: Ground level packages (green buttons)
- **Level 2**: Mid-height packages (yellow buttons)
- **Level 3**: High-level packages (red buttons)

## Implementation Notes

- The home position is dynamically retrieved from the HOME package in the database
- If the HOME package is not found, a default position (0,0,0) is used
- All coordinates are in the robot's coordinate system
- The level field helps the robot determine height requirements for navigation
- The format is consistent across all package types and the home command

## Error Handling

- If the database is unavailable, fallback coordinates are used
- Network errors are logged to the console
- Invalid package data is handled gracefully with default values 