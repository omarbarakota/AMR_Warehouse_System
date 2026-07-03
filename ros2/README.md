# ROS 2 workspace notes

This folder contains ROS 2-related components for the AMR warehouse system.

## MQTT bridge package

The package under [ros2/mqtt_ros2_bridge](ros2/mqtt_ros2_bridge) provides an MQTT-to-ROS 2 bridge node and launch file.

## Install Mosquitto

On Ubuntu/Debian:

```bash
sudo apt update
sudo apt install -y mosquitto mosquitto-clients
```

## Start the broker

```bash
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

## Current broker configuration

The default Mosquitto broker configuration is typically:

```bash
/etc/mosquitto/mosquitto.conf
```

A minimal working configuration is:

```conf
listener 1883
allow_anonymous true
persistence true
persistence_location /var/lib/mosquitto/
log_dest file /var/log/mosquitto/mosquitto.log
```

If you need to verify the broker is listening:

```bash
sudo ss -ltnp | grep 1883
```

If you need to inspect the service status:

```bash
sudo systemctl status mosquitto
```

## Launch the bridge

From the repository root, after sourcing your ROS 2 environment:

```bash
source /opt/ros/humble/setup.bash
ros2 launch ros2/mqtt_ros2_bridge/launch/mqtt_ros2_bridge.launch.py
```

If you want to override the broker host or prefix:

```bash
ros2 launch ros2/mqtt_ros2_bridge/launch/mqtt_ros2_bridge.launch.py mqtt_host:=localhost mqtt_topic_prefix:=/warehouse
```
