import os

class Settings:
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "database/app.db")
    DEBUG: bool = bool(os.getenv("DEBUG", True))

settings = Settings()