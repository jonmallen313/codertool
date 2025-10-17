import os
from typing import Dict
from src.agents.base import BaseAgent
from src.core.memory import Task
from src.integrations.github import GitHubClient

class CoderAgent(BaseAgent):
    def __init__(self, memory):
        super().__init__(memory)
        self.github = GitHubClient()
    
    async def handle_task(self, task: Task) -> Dict:
        """Handle code generation and modification tasks"""
        messages = [
            {
                "role": "system",
                "content": "You are an expert programmer. Generate or modify code based on the given requirements."
            },
            {
                "role": "user",
                "content": f"""
                Task: {task.description}
                Context: {self.format_context(task)}
                
                Please provide the implementation or code changes needed.
                """
            }
        ]
        
        response = await self.call_claude(messages)
        
        # Apply code changes
        success = await self._apply_changes(task, response)
        
        if success:
            # Commit and push changes
            await self.github.commit_and_push(
                files=[ctx.file_path for ctx in task.context if ctx.file_path],
                message=f"feat: {task.description}"
            )
            self.memory.update_task_status(task.id, "completed")
            return {"status": "success"}
        
        self.memory.update_task_status(task.id, "failed")
        return {"status": "failed", "error": "Failed to apply changes"}
    
    async def _apply_changes(self, task: Task, changes: str) -> bool:
        """Apply code changes to files"""
        try:
            # Implement code change logic here
            return True
        except Exception as e:
            self.memory.add_error({
                "task_id": task.id,
                "error": str(e),
                "type": "code_change_error"
            })
            return False