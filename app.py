
from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

ESP32_URL = "http://10.133.173.182"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/status")
def api_status():
    try:
        r = requests.get(ESP32_URL + "/status", timeout=3)
        rover_data = r.json()

        return jsonify({
            "project": "FIRE AI",
            "mode": "hardware",
            "alerts": [],
            "threshold": 1800,
            "dispatch_requested": False,
            "rover_moving": False,
            "devices": {
                "home_02": {
                    "status": "waiting",
                    "sensors": {
                        "gas": None,
                        "flame": None,
                        "temperature": None,
                        "distance": None
                    }
                },
                "rover": {
                    "status": rover_data.get("rover", "offline"),
                    "sensors": {
                        "gas": None,
                        "flame": None,
                        "temperature": None,
                        "distance": rover_data.get("distance")
                    }
                }
            }
        })
    except requests.RequestException:
        return jsonify({"error": "Rover disconnected"}), 503

@app.route("/api/camera-status")
def camera_status():
    return jsonify({"connected": False})

@app.route("/api/demo-alert", methods=["POST"])
def demo_alert():
    return jsonify({"message": "Demo alert endpoint active",
                    "simulated": True})

@app.route("/api/dispatch", methods=["POST"])
def dispatch():
    return jsonify({"message": "Dispatch request recorded",
                    "simulated": True})

@app.route("/api/clear-demo", methods=["POST"])
def clear_demo():
    return jsonify({"message": "Demo cleared"})

@app.route("/move/<direction>")
def move(direction):
    if direction not in ["F", "B", "L", "R", "S"]:
        return jsonify({"error": "Invalid direction"}), 400

    try:
        r = requests.get(
            ESP32_URL + "/move",
            params={"dir": direction},
            timeout=3
        )
        return jsonify({"result": r.text})
    except requests.RequestException:
        return jsonify({"error": "Rover disconnected"}), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
