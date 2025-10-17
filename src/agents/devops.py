from typing import Dict, List
from src.agents.base import BaseAgent
from src.core.memory import Task
from src.integrations.railway import RailwayClient

class DevOpsAgent(BaseAgent):
    def __init__(self, memory):
        super().__init__(memory)
        self.railway = RailwayClient()
    
    async def handle_task(self, task: Task) -> Dict:
        """Handle deployment and infrastructure tasks"""
        if task.type == "fix":
            return await self._handle_build_failure(task)
        
        messages = [
            {
                "role": "system",
                "content": "You are a DevOps expert. Analyze build logs and deployment issues."
            },
            {
                "role": "user",
                "content": f"""
                Task: {task.description}
                Context: {self.format_context(task)}
                
                Please analyze the deployment issue and suggest fixes.
                """
            }
        ]
        
        response = await self.call_claude(messages)
        
        # Create review task for suggested fixes
        review_task = Task(
            id=f"{task.id}_review",
            type="review",
            description="Review suggested deployment fixes",
            context=[{"content": response}],
            parent_task_id=task.id
        )
        self.memory.add_task(review_task)
        
        self.memory.update_task_status(task.id, "completed")
        return {"status": "success", "review_task": review_task.id}
    
    async def _handle_build_failure(self, task: Task) -> Dict:
        """Handle Railway build failures"""
        build_logs = await self.railway.get_build_logs(task.metadata.get("build_id"))
        
        # Create context with build logs
        task.context.append({
            "content": build_logs,
            "error_message": "Build failed"
        })
        
        messages = [
            {
                "role": "system",
                "content": "You are a DevOps expert. Analyze build failures and suggest fixes."
            },
            {
                "role": "user",
                "content": f"""
                Build Logs: {build_logs}
                Please analyze the build failure and suggest specific fixes.
                """
            }
        ]
        
        response = await self.call_claude(messages)
        
        # Create fix task
        fix_task = Task(
            id=f"{task.id}_fix",
            type="code",
            description="Apply build failure fixes",
            context=[{"content": response}],
            parent_task_id=task.id
        )
        self.memory.add_task(fix_task)
        
        self.memory.update_task_status(task.id, "completed")
        return {"status": "success", "fix_task": fix_task.id}