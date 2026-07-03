# MQTT Topics and Payloads Used by the Dashboard

This file documents the MQTT topics and payloads used by the control UI in [app/templates/index.html](app/templates/index.html) and [app/static/js/dashboard.js](app/static/js/dashboard.js).

Note:
- The front end sends its payload as a JSON string to the backend endpoint `/publish`.
- The backend forwards that message to the MQTT broker on the selected topic.
- The examples below show the payload content that is sent in the `message` field.

## Topics published by the UI

| Topic | Trigger / UI control | Payload shape | Example |
| --- | --- | --- | --- |
| `/robot/move` | Joystick movement | JSON object with `x` and `z` values | `{"x":0.12,"z":-0.25}` |
| `/robot/goal` | Package selection or Return Home | JSON object with either `target`/`delivery` or `home` | `{"target":{"x":1.2,"y":3.4,"theta":0.1,"level":2},"delivery":{"x":-3.03,"y":-1.65,"theta":2.13}}` |
| `/robot/goal` | Return Home | JSON object with `home` | `{"home":{"x":0.0,"y":0.0,"theta":0.0}}` |
| `/robot/lift` | Lift Up / Down / Stop | String command | `"liftup"`, `"liftdown"`, `"liftstop"` |
| `/robot/gripper` | Gripper On / Off | String command | `"gripperon"`, `"gripperoff"` |
| `/robot/grippermove` | Gripper Front / Back | String command | `"gripperfront"`, `"gripperback"` |
| `/robot/emergency` | Emergency Stop | String command | `"STOP"` |
| `/robot/arm/move` | Arm movement buttons | String command | `"armup"`, `"armdown"`, `"armleft"`, `"armright"`, `"rotate_cw"`, `"rotate_ccw"` |
| `/robot/arm/gripper` | Arm gripper Open / Close | String command | `"open"`, `"close"` |

## Payload details

### 1. Joystick movement
Topic: `/robot/move`

Example payload:
```json
{"x":0.12,"z":-0.25}
```

Used by the custom joystick in the dashboard.

### 2. Package goal
Topic: `/robot/goal`

Example payload:
```json
{
  "target": {
    "x": 1.2,
    "y": 3.4,
    "theta": 0.1,
    "level": 2
  },
  "delivery": {
    "x": -3.0328106,
    "y": -1.65626,
    "theta": 2.13
  }
}
```

### 3. Return home
Topic: `/robot/goal`

Example payload:
```json
{
  "home": {
    "x": 0.0,
    "y": 0.0,
    "theta": 0.0
  }
}
```

### 4. Lift commands
Topic: `/robot/lift`

Possible payload values:
- `"liftup"`
- `"liftdown"`
- `"liftstop"`

### 5. Gripper commands
Topic: `/robot/gripper`

Possible payload values:
- `"gripperon"`
- `"gripperoff"`

### 6. Gripper movement
Topic: `/robot/grippermove`

Possible payload values:
- `"gripperfront"`
- `"gripperback"`

### 7. Emergency stop
Topic: `/robot/emergency`

Example payload:
```json
"STOP"
```

### 8. Arm movement
Topic: `/robot/arm/move`

Possible payload values:
- `"armup"`
- `"armdown"`
- `"armleft"`
- `"armright"`
- `"rotate_cw"`
- `"rotate_ccw"`

### 9. Arm gripper
Topic: `/robot/arm/gripper`

Possible payload values:
- `"open"`
- `"close"`

## Topics subscribed by the UI

The dashboard also subscribes to these topics to update the UI state:

| Topic | Meaning | Expected payload |
| --- | --- | --- |
| `/robot/connection` | Robot connection state | Text such as `connected` or `disconnected` |
| `/robot/status` | Robot status or task text | Text such as `idle`, `package delivered`, `home reached`, or other task/status messages |

## Notes
- The dashboard UI uses these topics directly from [app/static/js/dashboard.js](app/static/js/dashboard.js).
- The HTML buttons in [app/templates/index.html](app/templates/index.html) trigger the corresponding publish functions.
- If you later change a topic or payload format, update this file so the interface contract stays documented.
