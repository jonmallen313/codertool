from typing import Dict, List
from src.agents.base import BaseAgent
from src.core.memory import Task
from src.integrations.github import GitHubClient

class ReviewerAgent(BaseAgent):
    def __init__(self, memory):
        super().__init__(memory)
        self.github = GitHubClient()
    
    async def handle_task(self, task: Task) -> Dict:
        """Handle code review and analysis tasks"""
        messages = [
            {
                "role": "system",
                "content": "You are an expert code reviewer. Analyze code changes and suggest improvements."
            },
            {
                "role": "user",
                "content": f"""
                Task: {task.description}
                Context: {self.format_context(task)}
                
                Please review the code/error and suggest specific improvements or fixes.
                """
            }
        ]
        
        response = await self.call_claude(messages)
        suggestions = self._parse_suggestions(response)
        
        if suggestions:
            # Create fix tasks for each suggestion
            fix_tasks = []
            for suggestion in suggestions:
                task_id = f"{task.id}_fix_{len(fix_tasks)}"
                fix_task = Task(
                    id=task_id,
                    type="code",
                    description=suggestion["description"],
                    context=suggestion.get("context", []),
                    parent_task_id=task.id
                )
                self.memory.add_task(fix_task)
                fix_tasks.append(task_id)
            
            self.memory.update_task_status(task.id, "completed")
            return {"status": "success", "fix_tasks": fix_tasks}
        
        self.memory.update_task_status(task.id, "failed")
        return {"status": "failed", "error": "No actionable suggestions found"}
    
    def _parse_suggestions(self, response: str) -> List[Dict]:
        """Parse Claude's response into structured suggestions"""
        # Implement parsing logic here
        # For now, return a simple example
        return [
            {
                "description": "Example fix suggestion",
                "context": []
            }
        ]