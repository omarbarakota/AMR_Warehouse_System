document.addEventListener('DOMContentLoaded', function() {
  const mapCanvas = document.getElementById('mapCanvas');
  const ctx = mapCanvas.getContext('2d');
  
  const mapImage = new Image();
  let robotPose = { x: 0, y: 0, theta: 0 };

  mapImage.onload = function() {
    mapCanvas.width = mapImage.width;
    mapCanvas.height = mapImage.height;
    robotPose.x = mapCanvas.width / 2;
    robotPose.y = mapCanvas.height / 2;
    robotPose.theta = 0;
    drawMap();
  };

  function drawMap() {
    ctx.clearRect(0, 0, mapCanvas.width, mapCanvas.height);
    ctx.drawImage(mapImage, 0, 0, mapCanvas.width, mapCanvas.height);
    drawRobot();
  }

  function drawRobot() {
    const robotSize = 20; // Robot's size
  
    ctx.save(); // Save current canvas state
  
    ctx.translate(robotPose.x, robotPose.y); // Move to robot's position
    ctx.rotate(robotPose.theta); // Rotate the canvas by robot's orientation
    
    // Draw a simple triangle pointing "up" by default
    ctx.beginPath();
    ctx.moveTo(0, -robotSize); // Tip of triangle (forward)
    ctx.lineTo(robotSize / 2, robotSize / 2); // Bottom right
    ctx.lineTo(-robotSize / 2, robotSize / 2); // Bottom left
    ctx.closePath();
    ctx.fillStyle = 'red';
    ctx.fill();
  
    ctx.restore(); // Restore canvas state
  }
  

  mapImage.src = '/static/img/map.png'; // Your placeholder map
});

/*
const canvas = document.getElementById("mapCanvas");
const ctx = canvas.getContext("2d");

const mapImg = new Image();
const robotImg = new Image();
mapImg.src = "/static/img/map.jpg";
robotImg.src = "/static/img/robot-icon.png";

let robotPose = { x: 0, y: 0, theta: 0 };

// Set up MQTT connection
const mqttBroker = "ws://localhost:9001"; // Ensure WebSocket is enabled on your broker
const client = mqtt.connect(mqttBroker);

client.on('connect', () => {
  console.log("Connected to MQTT broker");
  client.subscribe('/robot/pose');
});

client.on('message', (topic, message) => {
  try {
    const data = JSON.parse(message.toString());
    robotPose.x = data.x * 40;     // scale turtle pose to canvas
    robotPose.y = canvas.height - data.y * 40; // invert Y for canvas
    robotPose.theta = data.theta;
    drawScene();
  } catch (e) {
    console.error("Error parsing MQTT message:", e);
  }
});

function drawScene() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.drawImage(mapImg, 0, 0, canvas.width, canvas.height);

  ctx.save();
  ctx.translate(robotPose.x, robotPose.y);
  ctx.rotate(robotPose.theta);
  ctx.drawImage(robotImg, -20, -20, 40, 40);
  ctx.restore();
}

mapImg.onload = drawScene;
robotImg.onload = drawScene;
*/
