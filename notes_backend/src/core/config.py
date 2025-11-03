import os
from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Application settings loaded from environment variables."""
    app_name: str = Field(default="Smart Notes Manager - Notes API")
    environment: str = Field(default=os.getenv("ENVIRONMENT", "development"))
    # Reserved for future DB integration (not used now)
    # DATABASE_URL: Optional[str] = Field(default=os.getenv("DATABASE_URL"))


# Expose a singleton settings instance
settings = Settings()
