
    
    const manualtopic = '/turtle1/cmd_vel';
    
    // Function to send movement commands
    function moveRobot(topic, message) {
      client.publish(topic, message, (err) => {
        if (err) {
          console.error(`Failed to publish to ${manualtopic}:`, err.message);
        } else {
          console.log(`Published to ${manualtopic}:`, message);
        }
      });
    }

  // Button event listeners

  document.getElementById('btn-up').addEventListener('mouseup', () => moveRobot(manualtopic,'u1.5'));
  document.getElementById('btn-down').addEventListener('mousedown', () => moveRobot(manualtopic,'d1.5'));
  document.getElementById('btn-left').addEventListener('mousedown', () => moveRobot(manualtopic,'l1.5'));
  document.getElementById('btn-right').addEventListener('mousedown', () => moveRobot(manualtopic,'r1.5'));
  

