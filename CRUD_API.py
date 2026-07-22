import sqlite3
from fastapi import FastAPI
from fastapi.responses import JSONResponse,Response
from pydantic import BaseModel
from typing import Optional
import uvicorn

conn = sqlite3.connect("tasks.db",check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT, done BOOLEAN)")
total_tasks=cursor.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
if total_tasks==0:
    cursor.execute('INSERT INTO tasks (title, done) VALUES (?, ?)', ("Fold laundry",False))
    cursor.execute('INSERT INTO tasks (title, done) VALUES (?, ?)', ("Walk the dog",True))
    cursor.execute('INSERT INTO tasks (title, done) VALUES (?, ?)', ("Do assignments",False))
conn.commit()

app=FastAPI()

@app.get("/")
def task_API():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }
@app.get("/Health")
def health_check():
    return { "status": "OK" }
@app.get("/tasks")
def get_tasks():
    cursor = conn.execute("SELECT * FROM tasks")
    tasks = []
    for row in cursor.fetchall():
        tasks.append({"id": row[0], "title": row[1], "done": row[2]})
    return tasks

@app.get("/tasks/{id}")
def get_task(id: int):
   cursor = conn.execute("SELECT * FROM tasks WHERE id=?", (id,))
   row = cursor.fetchone()
   if row:
       return {"id": row[0], "title": row[1], "done": row[2]}
   else:
       return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})

class TaskCreate(BaseModel):
    title: str = ""
@app.post("/tasks")
def create_task(task: TaskCreate):
    if not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title cannot be empty"}
        )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (task.title, False))
    conn.commit()
    task_id = cursor.lastrowid
    return JSONResponse(status_code=201, content={"message": f"Task {task_id} created", "id": task_id, "title": task.title, "done": False})

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

@app.put("/tasks/{id}")
def update_task(id: int, update: TaskUpdate):
    if update.title is None and update.done is None:
        return JSONResponse(
            status_code=400,
            content={"error": "Provide a title or done value to update"}
        )
    if update.title is not None and not update.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title cannot be empty"}
        )
    
    cursor = conn.cursor()
    if update.title is not None:
        result=cursor.execute("UPDATE tasks SET title=? WHERE id=?", (update.title, id))
    if update.done is not None:
        result=cursor.execute("UPDATE tasks SET done=? WHERE id=?", (update.done, id))
    if cursor.rowcount == 0:
        return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})
    conn.commit()
    cursor.execute("SELECT * FROM tasks WHERE id=?", (id,))
    row = cursor.fetchone()
    return JSONResponse(status_code=200, content={"message": f"Task {id} updated", "id": id, "title": row[1], "done": row[2]})



@app.delete("/tasks/{id}")
def delete_task(id: int):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (id,))
    if cursor.rowcount == 0:
        return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})
    conn.commit()
    return Response(status_code=204)