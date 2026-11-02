import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Artemis Earth Detective"
    PROJECT_VERSION: str = "1.0.0"
    MODULE_NAME: str = "Artemis Earth Detective"
    ARTEMIS_AI_KEY: str = os.getenv("ARTEMIS_AI_KEY", "")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:[ARTEMISEARTH2026]@db.lqyvmdgxsfevkmzpsgww.supabase.co:5432/postgres"
    )

    class Config:
        case_sensitive = True

settings = Settings()