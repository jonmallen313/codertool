from typing import Dict, List
import anthropic
from src.core.memory import Task, SharedMemory

class BaseAgent:
    def __init__(self, memory: SharedMemory):
        self.memory = memory
        self.client = anthropic.Client(api_key="your-api-key")
        
    async def call_claude(self, messages: List[Dict], max_tokens: int = 1000):
        """Make an API call to Claude"""
        response = await self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=max_tokens,
            messages=messages
        )
        return response.content[0].text
    
    def format_context(self, task: Task) -> str:
        """Format task context for Claude prompt"""
        context = ""
        for ctx in task.context:
            if ctx.file_path:
                context += f"\nFile: {ctx.file_path}\n"
                if ctx.content:
                    context += f"Content:\n{ctx.content}\n"
                if ctx.error_message:
                    context += f"Error:\n{ctx.error_message}\n"
        return context