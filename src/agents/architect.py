from typing import List, Dict
from src.agents.base import BaseAgent
from src.core.memory import Task

class ArchitectAgent(BaseAgent):
    async def handle_task(self, task: Task) -> Dict:
        """Handle architecture planning tasks"""
        messages = [
            {
                "role": "system",
                "content": "You are an expert software architect. Break down tasks into clear, actionable subtasks."
            },
            {
                "role": "user",
                "content": f"""
                Task: {task.description}
                Context: {self.format_context(task)}
                
                Please break this task into smaller subtasks and provide architectural guidance.
                """
            }
        ]
        
        response = await self.call_claude(messages)
        
        # Parse response and create subtasks
        subtasks = self._parse_subtasks(response)
        for subtask in subtasks:
            task_id = f"{task.id}_subtask_{len(task.subtasks)}"
            new_task = Task(
                id=task_id,
                type="code",
                description=subtask["description"],
                context=subtask.get("context", []),
                parent_task_id=task.id
            )
            self.memory.add_task(new_task)
            task.subtasks.append(task_id)
        
        self.memory.update_task_status(task.id, "completed")
        return {"status": "success", "subtasks": task.subtasks}
    
    def _parse_subtasks(self, response: str) -> List[Dict]:
        """Parse Claude's response into structured subtasks"""
        # Implement parsing logic here
        # For now, return a simple example
        return [
            {
                "description": "Example subtask",
                "context": []
            }
        ]