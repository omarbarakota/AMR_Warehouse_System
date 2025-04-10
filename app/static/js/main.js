// Ensure you include the MQTT.js library in your HTML file
// Example: <script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>


// Connection Handlers
client.on('connect', () => {
  statusElement.textContent = 'Connected to MQTT Broker';
  console.log('Connected to MQTT Broker');
  
  // Create buttons for each topic
  createPublishButtons(topics);

  // Subscribe to all topics in the array
  subscribeToTopics(client, topics);
});

// Handle errors
client.on('error', (err) => {
  statusElement.textContent = 'Error: ' + err.message;
  console.error('MQTT Error:', err.message);
});

// Disconnect Handler
client.on('close', () => {
  statusElement.textContent = 'Disconnected from MQTT Broker';
  console.log('Disconnected from MQTT Broker');
});
