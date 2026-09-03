# TS Notes API (starter app for Assignment Question 3)

A tiny Express API written in TypeScript:

- `GET /` — app info
- `GET /notes` — list notes
- `POST /notes` — body `{"text": "..."}`, adds a note
- `GET /health` — health check

This app must be **compiled** before it can run — `npm run build` runs `tsc`
and produces `dist/index.js`, which is what actually executes. `npm run dev`
(via `ts-node`) will also work locally without a separate build step, which
is useful for confirming the app logic works before you containerize it.

Run locally to see expected behavior:

```bash
npm install
npm run build
npm start
curl localhost:3000/notes
```

You are not given a Dockerfile — writing a single-stage one and a
multi-stage one is the assignment.
