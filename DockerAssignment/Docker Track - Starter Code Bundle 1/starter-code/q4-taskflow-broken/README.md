# TaskFlow (starter app for Assignment Question 4)

A Flask + PostgreSQL task list, provided together with a Dockerfile and a
docker-compose.yml that **do not work correctly yet**.

## What "working" looks like

Once the container setup is correct:

```bash
docker compose up --build
curl -X POST localhost:8080/tasks -H "Content-Type: application/json" -d '{"title":"read the assignment"}'
curl localhost:8080/tasks
```

should return the created task, and repeated `docker compose up` /
`docker compose down` cycles should not lose previously saved tasks.

## Rules for this assignment

- **Do not modify `app.py`.** It is correct. The problems are in the
  Dockerfile and docker-compose.yml around it.
- The database name, user, and password are fixed by the assignment brief:
  `hudb` / `huuser` / `hupassword`. Keep these values.
- You may change anything in the Dockerfile and docker-compose.yml.

## App endpoints (for reference)

- `GET /` — app info
- `GET /tasks` — list tasks
- `POST /tasks` — body `{"title": "..."}`, adds a task
- `GET /health` — health check
