const manualtopic = '/turtle1/cmd_vel';

function moveRobot(topic, message) {
  client.publish(topic, message, (err) => {
    if (err) {
      console.error(`Failed to publish to ${manualtopic}:`, err.message);
    } else {
      console.log(`Published to ${manualtopic}:`, message);
    }
  });
}

// Ensure buttons exist before adding listeners
document.addEventListener('DOMContentLoaded', () => {
  const upBtn = document.getElementById('btn-up');
  const downBtn = document.getElementById('btn-down');
  const leftBtn = document.getElementById('btn-left');
  const rightBtn = document.getElementById('btn-right');
  const stopBtn = document.getElementById('btn-stop');

  if (upBtn) upBtn.addEventListener('mousedown', () => moveRobot(manualtopic, 'u1.5'));
  if (downBtn) downBtn.addEventListener('mousedown', () => moveRobot(manualtopic, 'd1.5'));
  if (leftBtn) leftBtn.addEventListener('mousedown', () => moveRobot(manualtopic, 'l1.5'));
  if (rightBtn) rightBtn.addEventListener('mousedown', () => moveRobot(manualtopic, 'r1.5'));
  if (stopBtn) stopBtn.addEventListener('mousedown', () => moveRobot(manualtopic, 's0'));
});
