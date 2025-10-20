from typing import Dict, List
import anthropic
from src.core.memory import Task, SharedMemory
from src.core.config import settings

class BaseAgent:
    def __init__(self, memory: SharedMemory):
        self.memory = memory
        self.client = anthropic.Client(api_key=settings.CLAUDE_API_KEY)
        
    async def call_claude(self, messages: List[Dict], max_tokens: int = 1000):
        """Make an API call to Claude"""
        formatted_messages = []
        
        for msg in messages:
            if msg["role"] == "user":
                formatted_messages.append({
                    "role": "user",
                    "content": msg["content"]
                })
            elif msg["role"] == "assistant":
                formatted_messages.append({
                    "role": "assistant",
                    "content": msg["content"]
                })
        
        response = await self.client.messages.create(
            messages=formatted_messages,
            model="claude-3-opus-20240229",
            max_tokens=max_tokens
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