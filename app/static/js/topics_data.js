        const topicElements = {};

        // Use topics from topics.js
        if (typeof topics === 'undefined') {
            console.error('Topics not found. Ensure topics.js is loaded.');
        } else {
            topics.forEach((topic) => {
                // Create UI elements for each topic
                const topicDiv = document.createElement('div');
                topicDiv.classList.add('topic');
                topicDiv.innerHTML = `
                    <h2>${topic}</h2>
                    <ul class="data-list" id="${topic}-list"></ul>
                `;
                topicsContainer.appendChild(topicDiv);
                topicElements[topic] = document.getElementById(`${topic}-list`);
            });

            // Subscribe to Topics
            client.on('connect', () => {
                console.log('Connected to MQTT Broker');
                topics.forEach((topic) => {
                    client.subscribe(topic, (err) => {
                        if (err) {
                            console.error(`Failed to subscribe to ${topic}`, err.message);
                        } else {
                            console.log(`Subscribed to ${topic}`);
                        }
                    });
                });
            });

            client.on('message', (topic, message) => {
                const data = document.createElement('li');
                data.textContent = message.toString();
                if (topicElements[topic]) {
                    topicElements[topic].appendChild(data);
                } else {
                    console.warn(`Received message for untracked topic: ${topic}`);
                }
            });

            client.on('error', (err) => {
                console.error('MQTT Error:', err.message);
            });
        }

        