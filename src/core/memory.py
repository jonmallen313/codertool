from typing import Dict, List, Optional
from pydantic import BaseModel

class CodeContext(BaseModel):
    file_path: str
    content: str
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    error_message: Optional[str] = None

class Task(BaseModel):
    id: str
    type: str  # "code", "review", "fix", "architecture"
    description: str
    context: List[CodeContext]
    metadata: Dict = {}
    parent_task_id: Optional[str] = None
    subtasks: List[str] = []
    status: str = "pending"  # pending, in_progress, completed, failed

class SharedMemory:
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.context_cache: Dict[str, Dict] = {}
        self.error_history: List[Dict] = []
        
    def add_task(self, task: Task):
        self.tasks[task.id] = task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)
    
    def update_task_status(self, task_id: str, status: str):
        if task_id in self.tasks:
            self.tasks[task_id].status = status
    
    def add_error(self, error_data: Dict):
        self.error_history.append(error_data)
    
    def get_related_context(self, task_id: str) -> Dict:
        return self.context_cache.get(task_id, {})