# Visitor Logger (starter app for Assignment Question 1)

A minimal Flask app with three endpoints:

- `GET /` — app info
- `POST /visit` — body `{"name": "someone"}`, appends a timestamped line to a log file
- `GET /visits` — returns every logged visit
- `GET /health` — basic health check

Configuration (read from environment variables at startup):

| Variable   | Default            | Purpose                        |
|------------|--------------------|---------------------------------|
| `APP_NAME` | `Visitor Logger`   | Name shown on `GET /`          |
| `PORT`     | `5000`             | Port the app listens on        |
| `LOG_FILE` | `/data/visits.log` | Path where visits are recorded |

Run locally (no Docker) to see expected behavior:

```bash
pip install -r requirements.txt
python app.py
curl -X POST localhost:5000/visit -H "Content-Type: application/json" -d '{"name":"vishal"}'
curl localhost:5000/visits
```

You are not given a Dockerfile — writing one is the assignment.
