// Ensure you include the MQTT.js library in your HTML file
// Example: <script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>



  // Connection Handlers
client.on('connect', () => {
    statusElement.textContent = 'Connected to MQTT Broker';
    console.log('Connected to MQTT Broker');
    

  
    // Subscribe to all topics in the array
    subscribeToTopics(client, topics);
});
  
  // Handle incoming messages
client.on('message', (topic, message) => {
    const li = document.createElement('li');
    li.textContent = `Topic: ${topic}, Message: ${message.toString()}`;
    messagesElement.appendChild(li);
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
  