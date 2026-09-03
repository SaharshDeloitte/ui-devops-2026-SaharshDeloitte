"""
Greeting API
A tiny Flask + PostgreSQL app used for the reverse-proxy / scaling assignment.

The `/` route returns the responding container's own hostname and a
request counter. That is deliberate: when you scale this service to
multiple replicas behind NGINX, repeated requests should show DIFFERENT
hostnames, which is your evidence that load balancing is actually
happening -- and during a rolling update, a steady stream of requests
against this endpoint should never show a dropped connection.
"""
import os
import socket
import time
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

VERSION = os.environ.get("APP_VERSION", "v1")
DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "hudb")
DB_USER = os.environ.get("DB_USER", "huuser")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "hupassword")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASSWORD,
    )


def init_db(retries=10, delay=3):
    for attempt in range(1, retries + 1):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS request_log (
                    id SERIAL PRIMARY KEY,
                    served_by TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                );
            """)
            conn.commit()
            cur.close()
            conn.close()
            print(f"[greeting-api] connected to postgres at {DB_HOST}:{DB_PORT}")
            return True
        except psycopg2.OperationalError as exc:
            print(f"[greeting-api] database not ready (attempt {attempt}/{retries}): {exc}")
            time.sleep(delay)
    print("[greeting-api] starting without a database connection")
    return False


@app.route("/")
def greet():
    hostname = socket.gethostname()
    count = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO request_log (served_by) VALUES (%s);", (hostname,))
        cur.execute("SELECT COUNT(*) FROM request_log;")
        count = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.OperationalError:
        pass
    return jsonify({
        "message": "hello from the Greeting API",
        "version": VERSION,
        "served_by": hostname,
        "total_requests": count,
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok", "served_by": socket.gethostname()})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
