let mouseMovements = [];
let gyroscopeData = [];
let touchEvents = [];
let deviceType = /Mobi|Android|iPhone|iPad/i.test(navigator.userAgent) ? "mobile" : "desktop";

document.getElementById("device_type").value = deviceType;

if (deviceType === "mobile") {
    window.addEventListener("deviceorientation", (event) => {
        gyroscopeData.push({
            alpha: event.alpha,
            beta: event.beta,
            gamma: event.gamma
        });
    });

    // Fix: Ensure at least one touch event is captured
    document.addEventListener("touchstart", (event) => {
        let touch = event.touches[0];
        touchEvents.push({ x: touch.clientX, y: touch.clientY });
    });

    document.addEventListener("touchmove", (event) => {
        let touch = event.touches[0];
        touchEvents.push({ x: touch.clientX, y: touch.clientY });
    });
}

document.addEventListener('mousemove', (event) => {
    if (deviceType === "desktop") {
        mouseMovements.push({ x: event.clientX, y: event.clientY });
    }
});

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("registerForm").addEventListener("submit", async function (event) {
        event.preventDefault();

        let username = document.getElementById("username").value.trim();
        let otp = document.getElementById("otp").value.trim();
        let hiddenName = document.getElementById("hidden_name").value.trim();
        let hiddenFieldDisplay = document.getElementById("hiddenFieldDisplay");

        if (username === "" || otp === "") {
            alert("All fields are required!");
            return;
        }

        hiddenFieldDisplay.innerHTML = `<strong>Hidden Field is filled:</strong> ${hiddenName}`;

        const postData = {
            username: username,
            otp: otp,
            hidden_name: hiddenName,
            device_type: deviceType,
            mouse_movements: mouseMovements,
            gyroscope_data: gyroscopeData,
            touch_events: touchEvents
        };

        try {
            const response = await fetch('/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(postData)
            });

            if (response.ok) {
                console.log('Data sent to the server successfully.');
                const data = await response.json();
                console.log('Response:', data);
                if (data.redirect) {
                    window.location.href = data.redirect;
                }
            } else {
                console.error('Failed to send data to the server.');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
});
