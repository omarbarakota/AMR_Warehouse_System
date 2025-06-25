// Ensure you include the MQTT.js library in your HTML file
// Example: <script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>


// Connection Handlers
client.on('connect', () => {
  statusElement.textContent = 'Connected to MQTT Broker';
  console.log('Connected to MQTT Broker');
  
  // Create buttons for each topic
  //createPublishButtons(topics);

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


client.on('message', function(topic, message) {
  if (topic === '/robot/map_image') {
    const base64Image = message.toString();
      mapImage.src = 'data:image/png;base64,' + base64Image;
      mapImage.onload = drawMap;
  }

  if (topic === '/robot/pose') {
   const poseData = JSON.parse(message.toString());
   // Scale position if needed
   robotPose.x = poseData.x * 10; // Example scaling
   robotPose.y = poseData.y * 10;
   robotPose.theta = poseData.theta;
   drawMap();
  }
});
