from fastapi import FastAPI
import uvicorn
app=FastAPI()

@app.get("/")
def task_API():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }
@app.get("/Health")
def health_check():
    return { "status": "OK" }
