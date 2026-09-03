"""
Visitor Logger
A tiny Flask app used for the Docker volumes & configuration assignment.

The app is intentionally simple: the assignment is about containerizing it
correctly (env-based config + persistent storage), not about the app logic.
"""
import os
import datetime
from datetime import timezone
from flask import Flask, request, jsonify

app = Flask(__name__)

APP_NAME = os.environ.get("APP_NAME", "Visitor Logger")
PORT = int(os.environ.get("PORT", 5000))
LOG_FILE = os.environ.get("LOG_FILE", "/data/visits.log")


def ensure_log_dir():
    log_dir = os.path.dirname(LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)


@app.route("/")
def home():
    return jsonify({
        "app": APP_NAME,
        "message": "POST a name to /visit, then GET /visits to see the log.",
        "log_file": LOG_FILE,
    })


@app.route("/visit", methods=["POST"])
def visit():
    data = request.get_json(silent=True) or {}
    name = data.get("name", "anonymous")
    timestamp = datetime.datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    line = f"{timestamp} - {name}\n"

    ensure_log_dir()
    with open(LOG_FILE, "a") as f:
        f.write(line)

    return jsonify({"status": "logged", "entry": line.strip()}), 201


@app.route("/visits")
def visits():
    ensure_log_dir()
    if not os.path.exists(LOG_FILE):
        return jsonify({"visits": []})
    with open(LOG_FILE) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return jsonify({"visits": lines, "count": len(lines)})


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    ensure_log_dir()
    app.run(host="0.0.0.0", port=PORT)
