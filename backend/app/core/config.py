"""Application Configuration and Environment Settings."""

import os
from typing import List
from pydantic import BaseModel


class Settings(BaseModel):
    """Central application configuration."""

    PROJECT_NAME: str = "SkillSync - AI Skill Gap Intelligence Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database: Default to sqlite file for zero-config local run, overridden by DATABASE_URL in docker
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./skillsync.db")

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "skillsync-super-secret-production-key-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "*"
    ]

    # LLM Providers
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")


settings = Settings()
