// All functions needed on the website

// Publish a message
function publishMessage() {
    const message = 'Hello from WebSocket Client!';
    fetch('/publish', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic: '/test/topic', message })
    });
    // Optionally, still publish directly for real-time UI if needed:
    // client.publish('/test/topic', message);
    console.log('Published message:', message);
}

/*function createPublishButtons(topics) {
    document.body.appendChild(buttonsContainer);
  
    topics.forEach((topic) => {
      // Create a button
      const button = document.createElement('button');
      button.textContent = `Publish to ${topic}`;
  
      // Add an event listener for publishing messages
      button.addEventListener('click', () => {
        const message = prompt(`Enter message for ${topic}:`, `Hello from WebSocket Client!`);
        if (message) {
          client.publish(topic, message, (err) => {
            if (err) {
              console.error(`Failed to publish to ${topic}:`, err.message);
            } else {
              console.log(`Published to ${topic}:`, message);
            }
          });
        }
      });
  
      // Add the button to the container
      buttonsContainer.appendChild(button);
    });
}
*/
// Function to subscribe to multiple topics
function subscribeToTopics(client, topics) {
    topics.forEach((topic) => {
      client.subscribe(topic, (err) => {
        if (err) {
          console.error(`Failed to subscribe to topic: ${topic}`, err.message);
        } else {
          console.log(`Subscribed to topic: ${topic}`);
        }
      });
    });
  }
  