// Connect to the MQTT Broker
const client = mqtt.connect('ws://localhost:9001', { // Corrected protocol
    clientId: 'web_client_' + Math.random().toString(16).slice(2),
    username: 'your_username', // Optional; set your broker's username
    password: 'your_password', // Optional; set your broker's password
  });

  
  