document.addEventListener('DOMContentLoaded', function () {
    const canControl = document.querySelector('.control-panel h4')?.textContent.includes('Robot Control');

    // Tab switching logic
    const btnMovement = document.getElementById("btn-movement");
    const btnOperations = document.getElementById("btn-operations");
    const movementControls = document.getElementById("movement-controls");
    const operationControls = document.getElementById("operation-controls");

    if (canControl && btnMovement && btnOperations) {
        btnMovement.onclick = function () {
            movementControls.style.display = "block";
            operationControls.classList.remove("active");
            this.classList.add("active");
            btnOperations.classList.remove("active");
        };

        btnOperations.onclick = function () {
            movementControls.style.display = "none";
            operationControls.classList.add("active");
            this.classList.add("active");
            btnMovement.classList.remove("active");
            loadPackages(); 
        };
    }

    // --- API & MQTT Functions ---
    
    async function loadPackages() {
        try {
            const response = await fetch('/api/packages');
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const packages = await response.json();
            
            const packageButtons = document.getElementById('package-buttons');
            packageButtons.innerHTML = ''; 
            
            packages.forEach(pkg => {
                if (pkg.package_id === 'HOME') return; // Don't show HOME as a button
                const button = document.createElement('button');
                button.className = 'btn btn-outline-primary';
                button.textContent = `${pkg.package_id}`;
                button.title = `${pkg.name} - Level: ${pkg.level}`;
                button.onclick = (event) => sendPackageGoal(pkg, event);
                packageButtons.appendChild(button);
            });
        } catch (error) {
            console.error('Error loading packages:', error);
            document.getElementById('package-buttons').innerHTML = '<p class="text-danger">Could not load packages.</p>';
        }
    }

    async function getHomePosition() {
        try {
            const response = await fetch('/api/packages');
            const packages = await response.json();
            const homePackage = packages.find(pkg => pkg.package_id === 'HOME');
            
            if (homePackage) {
                return { x: homePackage.x, y: homePackage.y, theta: homePackage.theta };
            }
            return { x: 0.0, y: 0.0, theta: 0.0 }; // Fallback
        } catch (error) {
            console.error('Error getting home position:', error);
            return { x: 0.0, y: 0.0, theta: 0.0 };
        }
    }

    // --- Global Functions for button onclick ---

    let lastSentX = 0;
    let lastSentZ = 0;
    let lastJoystickSent = 0;
    const JOYSTICK_THRESHOLD = 0.01; // More sensitive
    const JOYSTICK_THROTTLE_MS = 80; // Always send at least every 80ms

    function sendJoystickData(x, z) {
        const now = Date.now();
        const significantChange = Math.abs(x - lastSentX) >= JOYSTICK_THRESHOLD || Math.abs(z - lastSentZ) >= JOYSTICK_THRESHOLD;
        const timeElapsed = now - lastJoystickSent >= JOYSTICK_THROTTLE_MS;

        if (!significantChange && !timeElapsed) return;

        lastSentX = x;
        lastSentZ = z;
        lastJoystickSent = now;

        const payload = JSON.stringify({ x: x, z: z });
        fetch('/publish', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic: '/robot/move', message: payload })
        });
        console.log('[MQTT] Topic: /robot/move | Payload:', payload);
    }

    window.sendPackageGoal = async function(pkg, event) {
        let levelNumber = 1;
        if (pkg.level && pkg.level.startsWith('level')) {
            levelNumber = parseInt(pkg.level.replace('level', ''), 10) || 1;
        }
        const target = {
            x: pkg.x,
            y: pkg.y,
            theta: pkg.theta,
            level: levelNumber
        };
        // Fetch the current home location from the backend
        let delivery = { x: -3.0328106, y: -1.65626, theta: 2.13 };
        let home = { x: 0.0, y: 0.0, theta: 0.0 };
        try {
            const response = await fetch('/api/home-location');
            if (response.ok) {
                const homeData = await response.json();
                home = {
                    x: homeData.x,
                    y: homeData.y,
                    theta: homeData.theta
                };
                //delivery=home;
            }
        } catch (err) {
            console.error('Error fetching home location:', err);
        }
        const goalMsg = { target, delivery };
        const payload = JSON.stringify(goalMsg);
        fetch('/publish', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic: '/robot/goal', message: payload })
        });
        // Optionally, still publish directly for real-time UI if needed:
        // client.publish('/robot/goal', payload);
        console.log('[MQTT] Topic: /robot/goal | Payload:', payload);
        if (event && event.target) {
            const button = event.target;
            const originalText = button.textContent;
            button.textContent = `✓ Sent`;
            button.classList.remove('btn-outline-primary');
            button.classList.add('btn-success');
            setTimeout(() => {
                button.textContent = originalText;
                button.classList.remove('btn-success');
                button.classList.add('btn-outline-primary');
            }, 2000);
        }
    };

    window.sendGoal = async function(target) {
        if (target === 'home') {
            let home = { x: 0.0, y: 0.0, theta: 0.0 };
            try {
                const response = await fetch('/api/home-location');
                if (response.ok) {
                    const homeData = await response.json();
                    home = {
                        x: homeData.x,
                        y: homeData.y,
                        theta: homeData.theta
                    };
                }
            } catch (err) {
                console.error('Error fetching home location:', err);
            }
            const goalMsg = { home };
            const payload = JSON.stringify(goalMsg);
            fetch('/publish', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ topic: '/robot/goal', message: payload })
            });
            // Optionally, still publish directly for real-time UI if needed:
            // client.publish('/robot/goal', payload);
            console.log('[MQTT] Topic: /robot/goal | Payload:', payload);
        }
    };

    window.sendLiftCommand = (command) => {
        const payload = JSON.stringify(command);
        fetch('/publish', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic: '/robot/lift', message: payload })
        });
        // Optionally, still publish directly for real-time UI if needed:
        // client.publish('/robot/lift', payload);
        console.log('[MQTT] Topic: /robot/lift | Payload:', payload);
    };
    window.sendGripperCommand = (command) => {
        const payload = JSON.stringify(command);
        fetch('/publish', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic: '/robot/gripper', message: payload })
        });
        // Optionally, still publish directly for real-time UI if needed:
        // client.publish('/robot/gripper', payload);
        console.log('[MQTT] Topic: /robot/gripper | Payload:', payload);
    };
    window.sendGripperMoveCommand = (command) => {
        const payload = JSON.stringify(command);
        fetch('/publish', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic: '/robot/grippermove', message: payload })
        });
        // Optionally, still publish directly for real-time UI if needed:
        // client.publish('/robot/grippermove', payload);
        console.log('[MQTT] Topic: /robot/grippermove | Payload:', payload);
    };
    window.sendEmergencyStop = () => {
        const payload = JSON.stringify('STOP');
        fetch('/publish', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic: '/robot/emergency', message: payload })
        });
        // Optionally, still publish directly for real-time UI if needed:
        // client.publish('/robot/emergency', payload);
        console.log('[MQTT] Topic: /robot/emergency | Payload:', payload);
    };

    // --- Joystick (Custom, No NippleJS) ---
    function setupCustomJoystick() {
        const joystickBase = document.querySelector('.joystick-base');
        const joystickHandle = document.getElementById('joystick-handle');
        const xValue = document.getElementById('x-value');
        const zValue = document.getElementById('z-value');
        if (!joystickBase || !joystickHandle || !xValue || !zValue) return;

        let isDragging = false;
        let centerX, centerY, radius;

        function updateJoystickPosition(clientX, clientY) {
            const rect = joystickBase.getBoundingClientRect();
            centerX = rect.left + rect.width / 2;
            centerY = rect.top + rect.height / 2;
            radius = rect.width / 2 - 15; // 15 is half of handle size

            const deltaX = clientX - centerX;
            const deltaY = clientY - centerY;
            const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);

            let limitedX = deltaX, limitedY = deltaY;
            if (distance > radius) {
                const angle = Math.atan2(deltaY, deltaX);
                limitedX = radius * Math.cos(angle);
                limitedY = radius * Math.sin(angle);
            }

            joystickHandle.style.left = (rect.width / 2 + limitedX) + 'px';
            joystickHandle.style.top = (rect.height / 2 + limitedY) + 'px';

            // Normalized values (-1 to 1)
            const normalizedX = Math.max(-1, Math.min(1, limitedX / radius));
            const normalizedZ = Math.max(-1, Math.min(1, -limitedY / radius)); // Invert Y for Z

            // Scale to max values
            const scaledX = (normalizedZ * 0.32).toFixed(2); // Use Z for X (UP/DOWN)
            const scaledZ = (normalizedX * 0.5).toFixed(2);  // Use X for Z (LEFT/RIGHT)

            // Clamp
            const finalX = Math.max(-0.32, Math.min(0.32, parseFloat(scaledX)));
            const finalZ = Math.max(-0.5, Math.min(0.5, parseFloat(scaledZ)));

            xValue.textContent = finalX.toFixed(2);
            zValue.textContent = finalZ.toFixed(2);

            sendJoystickData(finalX, finalZ);
        }

        function resetJoystick() {
            joystickHandle.style.left = '50%';
            joystickHandle.style.top = '50%';
            joystickHandle.style.transform = 'translate(-50%, -50%)';
            xValue.textContent = '0.00';
            zValue.textContent = '0.00';
            sendJoystickData(0, 0);
        }

        // Mouse events
        joystickBase.addEventListener('mousedown', (e) => {
            isDragging = true;
            updateJoystickPosition(e.clientX, e.clientY);
        });
        document.addEventListener('mousemove', (e) => {
            if (isDragging) {
                updateJoystickPosition(e.clientX, e.clientY);
            }
        });
        document.addEventListener('mouseup', () => {
            if (isDragging) {
                isDragging = false;
                resetJoystick();
            }
        });

        // Touch events
        joystickBase.addEventListener('touchstart', (e) => {
            e.preventDefault();
            isDragging = true;
            const touch = e.touches[0];
            updateJoystickPosition(touch.clientX, touch.clientY);
        });
        document.addEventListener('touchmove', (e) => {
            if (isDragging) {
                e.preventDefault();
                const touch = e.touches[0];
                updateJoystickPosition(touch.clientX, touch.clientY);
            }
        });
        document.addEventListener('touchend', () => {
            if (isDragging) {
                isDragging = false;
                resetJoystick();
            }
        });

        // Initial reset
        resetJoystick();
    }

    // Replace NippleJS init with custom joystick
    if (document.querySelector('.analog-joystick-container')) {
        setupCustomJoystick();
    }

    if (canControl) {
        setupCustomJoystick();
    }

    // --- MQTT Live Status/Connection Updates ---
    if (typeof client !== 'undefined') {
        client.subscribe('/robot/connection');
        client.subscribe('/robot/status');
        client.on('message', function(topic, message) {
            if (topic === '/robot/connection') {
                const el = document.getElementById('connection-status');
                const statusEl = document.getElementById('robot-status');
                const taskEl = document.getElementById('current-task');
                if (!el) return;
                const msg = message.toString();
                el.textContent = msg;
                if (msg.trim().toLowerCase() === 'connected') {
                    el.classList.remove('bg-danger');
                    el.classList.add('bg-success');
                    // Set current task to 'Idle' when connected
                    if (taskEl) {
                        taskEl.textContent = 'Idle';
                        statusEl.textContent = 'Non-operational';
                        statusEl.classList.remove('bg-success');
                        statusEl.classList.add('bg-danger');
                    }
                } else if (msg.trim().toLowerCase() === 'disconnected') {
                    el.classList.remove('bg-success');
                    el.classList.add('bg-danger');
                    // Also update status and task to 'Disconnected'
                    if (statusEl) {
                        statusEl.textContent = 'Disconnected';
                        statusEl.classList.remove('bg-success');
                        statusEl.classList.add('bg-danger');
                    }
                    if (taskEl) {
                        taskEl.textContent = 'Disconnected';
                    }
                } else {
                    el.classList.remove('bg-success');
                    el.classList.add('bg-danger');
                }
            }
            if (topic === '/robot/status') {
                const statusEl = document.getElementById('robot-status');
                const taskEl = document.getElementById('current-task');
                if (!statusEl || !taskEl) return;
                const msg = message.toString();
                // Always display the incoming message as the current task
                taskEl.textContent = msg;
                // Status logic
                const lowered = msg.trim().toLowerCase();
                if (['idle', 'package delivered', 'home reached','emergency'].includes(lowered)) {
                    statusEl.textContent = 'Non-operational';
                    statusEl.classList.remove('bg-success');
                    statusEl.classList.add('bg-danger');
                } else {
                    statusEl.textContent = 'Operational';
                    statusEl.classList.remove('bg-danger');
                    statusEl.classList.add('bg-success');
                }
            }
        });
    }
}); 