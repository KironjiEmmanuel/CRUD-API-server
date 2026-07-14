from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Finish FastAPI tutorial", "done": True},
    {"id": 3, "title": "Walk the dog", "done": False},
]
import uvicorn
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
        raise HTTPException(status_code=404, detail=f"Task {id} not found")
    
   class TaskCreate(BaseModel):
    title: str = ""

@app.post("/tasks")
def create_task(task: TaskCreate):
    if not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )

    next_id = max((t["id"] for t in tasks), default=0) + 1
    new_task = {"id": next_id, "title": task.title, "done": False}
    tasks.append(new_task)

    return JSONResponse(status_code=201, content=new_task)