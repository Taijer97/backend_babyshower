from pydantic import BaseModel, field_validator
import os

class Settings(BaseModel):
    app_name: str = "baby-shower-backend"
    database_url: str = os.getenv("DATABASE_URL", "")
    allowed_origins: list[str] = (
        os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001,http://localhost:3004")
        .split(",")
    )

    @field_validator("database_url")
    @classmethod
    def ensure_mysql(cls, v: str) -> str:
        if not v:
            raise ValueError("DATABASE_URL es requerido")
        if not (v.startswith("mysql+aiomysql://") or v.startswith("mysql+pymysql://")):
            raise ValueError("DATABASE_URL debe usar MySQL (mysql+aiomysql o mysql+pymysql)")
        return v

settings = Settings()
