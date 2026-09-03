/**
 * TS Notes API
 * A tiny Express + TypeScript app used for the multi-stage build assignment.
 *
 * The point of this app is that it MUST be compiled (tsc) before it can run.
 * That build step is what makes the single-stage vs. multi-stage comparison
 * meaningful: a single-stage image ships the TypeScript compiler, dev
 * dependencies, and source alongside the compiled output; a multi-stage
 * image ships only the compiled JavaScript and production dependencies.
 */
import express, { Request, Response } from "express";

const app = express();
app.use(express.json());

const PORT = parseInt(process.env.PORT || "3000", 10);

interface Note {
  id: number;
  text: string;
}

const notes: Note[] = [];
let nextId = 1;

app.get("/", (_req: Request, res: Response) => {
  res.json({ app: "TS Notes API", endpoints: ["GET /notes", "POST /notes", "GET /health"] });
});

app.get("/notes", (_req: Request, res: Response) => {
  res.json({ notes, count: notes.length });
});

app.post("/notes", (req: Request, res: Response) => {
  const text = req.body?.text;
  if (!text) {
    return res.status(400).json({ error: "field 'text' is required" });
  }
  const note: Note = { id: nextId++, text };
  notes.push(note);
  return res.status(201).json(note);
});

app.get("/health", (_req: Request, res: Response) => {
  res.json({ status: "ok" });
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`TS Notes API listening on port ${PORT}`);
});
