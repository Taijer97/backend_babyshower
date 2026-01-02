from pydantic import BaseModel
import os

class Settings(BaseModel):
    app_name: str = "baby-shower-backend"
    database_url: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./backend.db")
    allowed_origins: list[str] = (
        os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001,http://localhost:3004")
        .split(",")
    )

settings = Settings()
