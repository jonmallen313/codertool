from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Keys and Tokens
    CLAUDE_API_KEY: str
    GITHUB_TOKEN: str
    RAILWAY_API_KEY: Optional[str] = None
    
    # Service URLs
    GITHUB_API_URL: str = "https://api.github.com"
    RAILWAY_API_URL: str = "https://railway.app/api/v2"
    
    # Agent Configuration
    MAX_RETRIES: int = 3
    TOKEN_LIMIT: int = 100000  # Claude context window limit
    TASK_QUEUE_SIZE: int = 100
    
    # Project Settings
    REPO_OWNER: str
    REPO_NAME: str
    MAIN_BRANCH: str = "main"
    
    class Config:
        env_file = ".env"

settings = Settings()