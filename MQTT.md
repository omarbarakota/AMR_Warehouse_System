# Best Practices

QoS
  QoS0: Message loss is acceptable and Queeing ins't required **Never Queued**
  QoS1: Default, Acceptable badnwidth and delivary guraantee
  QoS2: Message loss is acceptable and Queeing ins't required

clean session false -> Broker remember the session
presistant session -> broker remember info subs cannot miss data
  check messages expiry because some brokers delete old sessions and msgs

retained msgs:
 last msg the broker has, useful for start condition and if the sub disconnects
 solve initial data, can only store one data per topic

retained-> on topic context new subs recieves data immediatly
vs
queued-> on client context broker queue undelivered msgs

Last will testment (LWT): notification to all clients when any client disconnects
network failure, io problem, client fail to communicate in keep alive period
client doesnt send disconnect packet before network closing
best practice online offline 3l4an fl awl yb3t online wlma ysfl yb3t offline

half open TCP client disconnect but the broker doesn't know
keep alive mechanism kol ftra mo3yana  bytb3t pingreq pongreq mostly 60sec
client take over
best practice client unique client IDs
auth to prevent unwanted takeovers

ROS
Mobile
other devices

m3aya l map
robot hy3ml map w n7otha 3la l server manually

n4t8l mo2ktn 3la l arkam l mfrod n3ml client bytb3t data
ros hyb3t 3la topic mo3yn

## 1. Local MQTT Broker Address

If you’re running Mosquitto (or another broker) on your local machine:

Address: localhost or 127.0.0.1
Default Ports:
MQTT (unsecured): 1883
MQTT over SSL/TLS: 8883
MQTT over WebSocket: 8083 (if configured)

## 3. Public Broker Address

If the broker is hosted on a cloud server or external device:

Use the public IP address or domain name of the server.

Example: mqtt.example.com or 198.51.100.10
Confirm the broker’s port configuration in its settings.

Ensure the server's firewall allows incoming connections to the broker's port:

sudo ufw allow 1883
Test connection using mosquitto_pub or telnet:

mosquitto_pub -h mqtt.example.com -p 1883 -t test/topic -m "Test Message"

## 4. Test Broker Accessibility

To verify that the broker is reachable:

Use the mosquitto_sub client:

mosquitto_sub -h "broker-address" -p "port" -t test/topic
Publish a message:

mosquitto_pub -h "broker-address" -p "port" -t test/topic -m "Hello, MQTT!"

## 5. Broker Discovery (Dynamic IP)

If your broker uses a dynamic IP:

Use a service like Dynamic DNS (DDNS) to map the dynamic IP to a domain name.
Example: mqtt.dynamicdns.net

## 6. Check Mosquitto Logs

If unsure of your Mosquitto broker setup, check the logs for confirmation:

sudo tail -f /var/log/mosquitto/mosquitto.log
The logs will show:

The broker's listening address (e.g., 127.0.0.1 or 0.0.0.0 for all interfaces).
Any errors or misconfigurations.

## 7. If Using Docker

If the broker runs in a Docker container:

Check the container's IP:

docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "container-name"
Map ports in the docker run command or Docker Compose file.

Example:

yaml
ports:

- "1883:1883"
- "8883:8883"
Use the host machine's IP to access the broker
