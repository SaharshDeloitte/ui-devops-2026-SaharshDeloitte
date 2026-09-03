"""
TaskFlow API
A tiny Flask + PostgreSQL task list used for the container-debugging assignment.

The application code is correct and is NOT part of what you need to fix --
the assignment is about diagnosing and correcting the Dockerfile and
docker-compose.yml around it. Do not modify this file.
"""
import os
import time
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
PORT = int(os.environ.get("PORT", 8000))


def get_connection():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASSWORD,
    )


def init_db(retries=10, delay=3):
    """Create the tasks table if it doesn't exist yet. Retries briefly in
    case the database container is still starting up."""
    for attempt in range(1, retries + 1):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL
                );
            """)
            conn.commit()
            cur.close()
            conn.close()
            print(f"[taskflow] connected to postgres at {DB_HOST}:{DB_PORT}")
            return True
        except psycopg2.OperationalError as exc:
            print(f"[taskflow] database not ready (attempt {attempt}/{retries}): {exc}")
            time.sleep(delay)
    print("[taskflow] giving up waiting for the database")
    return False


@app.route("/")
def home():
    return jsonify({"app": "TaskFlow", "db_host": DB_HOST, "db_name": DB_NAME})


@app.route("/tasks", methods=["GET"])
def list_tasks():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title FROM tasks ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({"tasks": [{"id": r[0], "title": r[1]} for r in rows]})


@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    if not title:
        return jsonify({"error": "field 'title' is required"}), 400
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title) VALUES (%s) RETURNING id;", (title,))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": new_id, "title": title}), 201


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=PORT)
