from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import Field

class Settings(BaseSettings):
    # API Keys and Tokens
    CLAUDE_API_KEY: str = Field(..., env='CLAUDE_API_KEY')
    GITHUB_TOKEN: str = Field(..., env='GITHUB_TOKEN')
    RAILWAY_API_KEY: Optional[str] = Field(None, env='RAILWAY_API_KEY')
    
    # Service URLs
    GITHUB_API_URL: str = Field("https://api.github.com", env='GITHUB_API_URL')
    RAILWAY_API_URL: str = Field("https://railway.app/api/v2", env='RAILWAY_API_URL')
    
    # Agent Configuration
    MAX_RETRIES: int = Field(3, env='MAX_RETRIES')
    TOKEN_LIMIT: int = Field(100000, env='TOKEN_LIMIT')  # Claude context window limit
    TASK_QUEUE_SIZE: int = Field(100, env='TASK_QUEUE_SIZE')
    
    # Project Settings
    REPO_OWNER: str = Field(..., env='REPO_OWNER')
    REPO_NAME: str = Field(..., env='REPO_NAME')
    MAIN_BRANCH: str = Field("main", env='MAIN_BRANCH')
    
    # Server Settings
    HOST: str = Field("127.0.0.1", env='HOST')
    PORT: int = Field(8000, env='PORT')
    DEBUG: bool = Field(True, env='DEBUG')
    
    class Config:
        env_file = ".env"

settings = Settings()