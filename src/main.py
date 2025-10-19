from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
import uvicorn

from src.core.config import settings
from src.core.memory import SharedMemory, Task
from src.agents.architect import ArchitectAgent
from src.agents.coder import CoderAgent
from src.agents.reviewer import ReviewerAgent
from src.agents.devops import DevOpsAgent

app = FastAPI(title="Claude Multi-Agent System", debug=settings.DEBUG)
memory = SharedMemory()

# Initialize agents
architect = ArchitectAgent(memory)
coder = CoderAgent(memory)
reviewer = ReviewerAgent(memory)
devops = DevOpsAgent(memory)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/tasks/")
async def create_task(task: Task):
    """Create a new task and delegate to appropriate agent"""
    memory.add_task(task)
    
    if task.type == "architecture":
        return await architect.handle_task(task)
    elif task.type == "code":
        return await coder.handle_task(task)
    elif task.type == "review":
        return await reviewer.handle_task(task)
    elif task.type == "fix":
        return await devops.handle_task(task)
    else:
        raise HTTPException(status_code=400, message="Invalid task type")

@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    """Get status of a specific task"""
    task = memory.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/webhooks/railway")
async def railway_webhook(payload: Dict):
    """Handle Railway build/deploy webhooks"""
    if payload.get("status") == "failed":
        # Create review task for build failure
        task = Task(
            id=f"fix_{payload['id']}",
            type="review",
            description="Review Railway build failure",
            context=[{"error_message": payload.get("error")}]
        )
        memory.add_task(task)
        await reviewer.handle_task(task)
    return {"status": "processing"}

@app.post("/webhooks/github")
async def github_webhook(payload: Dict):
    """Handle GitHub push and PR webhooks"""
    # Handle different GitHub event types
    return {"status": "processing"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)