# Task API

A simple Task API for practicing backend fundamentals (routing, validation,
status codes) and, in this stage, persistent storage.

**Stack:** Python + FastAPI, SQLite for storage.

## Endpoints

| Method | Path          | Description                     |
|--------|---------------|----------------------------------|
| GET    | `/tasks`      | List all tasks                   |
| GET    | `/tasks/{id}` | Get a single task                |
| POST   | `/tasks`      | Create a task                    |
| PUT    | `/tasks/{id}` | Update a task's title and/or done|
| DELETE | `/tasks/{id}` | Delete a task                    |

Unknown ids return `404` with `{"error": "Task {id} not found"}`.
Invalid input (e.g. empty title) returns `400` with an `{"error": "..."}` body.

## Database

### Why SQLite?
SQLite was chosen because it stores the entire database in a single file,
with no separate database server to install or run — unlike MySQL or
PostgreSQL, which require a running server process. For a small project
like this, that made it simple to set up and easy to inspect directly.

### Where the database lives
The database file is `tasks.db`, created automatically in the project root
the first time the app runs — i.e. wherever you launch `uvicorn` from.
The `tasks` table is also created automatically if it doesn't exist, and
three example tasks are inserted only the first time the table is empty
(so restarting the server never duplicates them).

### How to run this project
```bash
pip install fastapi uvicorn
uvicorn CRUD_API:app --reload
```
The API will be available at `http://localhost:8000`, with interactive docs
at `http://localhost:8000/docs`. On first run, `tasks.db` is created
automatically with three example tasks. On later runs, your existing data
is loaded from that same file.

### Inspecting the database directly
Open `tasks.db` with [DB Browser for SQLite](https://sqlitebrowser.org/)
to view or edit data outside the API. Note: changes made in DB Browser
aren't visible to the running app until you click **Write Changes** — until
then they're only staged inside DB Browser, not yet written to the file.

![Database viewer screenshot](PASTE_SCREENSHOT_HERE.png)

### Example query
Run directly against `tasks.db` (e.g. in DB Browser's **Execute SQL** tab):

```sql
SELECT * FROM tasks WHERE done = 1;
```

This returns every task currently marked complete — useful for confirming
that the API and the database file always agree, since the API reads from
this same table on every request.

## Notes on design decisions
- Errors always use the shape `{"error": "..."}`, not FastAPI's default
  `{"detail": "..."}`.
- `PUT` supports partial updates (title and/or done).
- `DELETE` returns `204` with an empty body on success.
- The SQLite connection is opened with `check_same_thread=False`, since
  FastAPI runs synchronous route handlers in a thread pool rather than the
  main thread that created the connection.
