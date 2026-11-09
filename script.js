
const connectionStatus = document.getElementById("connectionStatus");
const pumpStatus = document.getElementById("pumpStatus");
const pumpState = document.getElementById("pumpState");

async function sendCommand(url) {
    try {
        const response = await fetch(url);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Command failed");
        }

        connectionStatus.textContent = "CONNECTED";
        return data;
    } catch (error) {
        connectionStatus.textContent = "CONNECTION ERROR";
        console.error(error);
        return null;
    }
}

// Rover movement
document.querySelectorAll(".move").forEach(button => {
    button.addEventListener("click", async () => {
        const direction = button.dataset.direction;
        await sendCommand(`/move/${direction}`);
    });
});

// Stop rover
document.getElementById("stopBtn").addEventListener("click", async () => {
    await sendCommand("/move/S");
});

// Pump ON
document.getElementById("pumpOn").addEventListener("click", async () => {
    const result = await sendCommand("/pump/on");

    if (result) {
        pumpStatus.textContent = "Pump: ON";
        pumpState.textContent = "ON";
    }
});

// Pump OFF
document.getElementById("pumpOff").addEventListener("click", async () => {
    const result = await sendCommand("/pump/off");

    if (result) {
        pumpStatus.textContent = "Pump: OFF";
        pumpState.textContent = "OFF";
    }
});

// Check rover connection
async function checkRover() {
    try {
        const response = await fetch("/api/status");
        const data = await response.json();

        if (!response.ok) throw new Error("Disconnected");

        const status = data.devices.rover.status;
        connectionStatus.textContent =
            status === "online" ? "ROVER ONLINE" : "ROVER WAITING";
    } catch {
        connectionStatus.textContent = "ROVER OFFLINE";
    }
}

checkRover();
setInterval(checkRover, 3000);
