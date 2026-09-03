# QuickTasks (starter app for Assignment Question 2)

A minimal Flask + Redis task list:

- `GET /` — app info (shows which Redis host/port it's configured for)
- `GET /tasks` — list all tasks
- `POST /tasks` — body `{"task": "buy milk"}`, appends a task
- `GET /health` — reports whether Redis is reachable

Configuration (environment variables):

| Variable     | Default | Purpose               |
|--------------|---------|------------------------|
| `REDIS_HOST` | `redis` | Redis service hostname |
| `REDIS_PORT` | `6379`  | Redis service port     |
| `PORT`       | `5000`  | Port the app listens on|

Run locally against a local Redis to see expected behavior:

```bash
pip install -r requirements.txt
REDIS_HOST=localhost python app.py
curl -X POST localhost:5000/tasks -H "Content-Type: application/json" -d '{"task":"buy milk"}'
curl localhost:5000/tasks
```

You are not given a Dockerfile or docker-compose.yml — writing both is the assignment.
