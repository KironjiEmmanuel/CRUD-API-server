from fastapi import FastAPI
from fastapi.responses import JSONResponse,Response
from pydantic import BaseModel
from typing import Optional
import uvicorn
tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Finish FastAPI tutorial", "done": True},
    {"id": 3, "title": "Walk the dog", "done": False},
]

app=FastAPI()

@app.get("/")
def task_API():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }
@app.get("/Health")
def health_check():
    return { "status": "OK" }
@app.get("/tasks")
def get_tasks():
    return tasks  
@app.get("/tasks/{id}")
def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task 
        
class TaskCreate(BaseModel):
    title: str = ""
@app.post("/tasks")
def create_task(task: TaskCreate):
    if not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title  cannot be empty"}
        )

    next_id = max((t["id"] for t in tasks), default=0) + 1
    new_task = {"id": next_id, "title": task.title, "done": False}
    tasks.append(new_task)

    return JSONResponse(status_code=201, content=new_task)

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
    
    for task in tasks:
        if task["id"] == id:
            if update.title is not None:
                task["title"] = update.title
            if update.done is not None:
                task["done"] = update.done
            return task

    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})


@app.delete("/tasks/{id}")
def delete_task(id: int):
    for i, task in enumerate(tasks):
        if task["id"] == id:
            tasks.pop(i)
            return Response(status_code=204)

    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})
