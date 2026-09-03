"""
QuickTasks API
A tiny Flask + Redis task tracker used for the Docker Compose assignment.

The app itself is intentionally simple: the assignment is about correctly
orchestrating it (networking, config, dependency ordering, persistence),
not about the application logic.
"""
import os
import time
import redis
from flask import Flask, request, jsonify

app = Flask(__name__)

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
TASKS_KEY = "quicktasks:tasks"

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def wait_for_redis(retries=5, delay=2):
    """Small built-in retry so the app fails with a clear log line instead of
    an unhandled crash if Redis isn't ready yet. This does NOT replace a
    proper 'wait for DB readiness' pattern at the orchestration level --
    that's part of what the assignment asks you to design."""
    for attempt in range(1, retries + 1):
        try:
            r.ping()
            print(f"[quicktasks] connected to redis at {REDIS_HOST}:{REDIS_PORT}")
            return True
        except redis.exceptions.ConnectionError as exc:
            print(f"[quicktasks] redis not ready (attempt {attempt}/{retries}): {exc}")
            time.sleep(delay)
    return False


@app.route("/")
def home():
    return jsonify({
        "app": "QuickTasks",
        "redis_host": REDIS_HOST,
        "redis_port": REDIS_PORT,
        "endpoints": ["GET /tasks", "POST /tasks", "GET /health"],
    })


@app.route("/tasks", methods=["GET"])
def list_tasks():
    tasks = r.lrange(TASKS_KEY, 0, -1)
    return jsonify({"tasks": tasks, "count": len(tasks)})


@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json(silent=True) or {}
    task = data.get("task")
    if not task:
        return jsonify({"error": "field 'task' is required"}), 400
    r.rpush(TASKS_KEY, task)
    return jsonify({"status": "added", "task": task}), 201


@app.route("/health")
def health():
    try:
        r.ping()
        return jsonify({"status": "ok", "redis": "connected"})
    except redis.exceptions.ConnectionError:
        return jsonify({"status": "degraded", "redis": "unreachable"}), 503


if __name__ == "__main__":
    wait_for_redis()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
