# Greeting API (starter app for Assignment Question 5)

A Flask + PostgreSQL app plus a starter NGINX config.

- `GET /` — logs the request to Postgres and returns the responding
  container's own **hostname**, the app **version**, and a running
  **request count**. The hostname is the key field: when this service is
  scaled to multiple replicas, different requests should be served by
  different hostnames.
- `GET /health` — health check.

Configuration (environment variables): `APP_VERSION`, `DB_HOST`, `DB_PORT`,
`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `PORT` (see defaults in `app.py`).

`nginx/nginx.conf` is a starting point, not a finished config -- it proxies
to a service named `api`, which is the name you should give the Flask
service in your compose file. You will likely need to adjust it once you
get to the rolling-update part of the assignment.

You are not given a Dockerfile or a docker-compose.yml -- writing those,
scaling the api service, and safely updating it is the assignment.
