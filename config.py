import os

class Settings:
    APP_NAME = "Afghan Digital Library API"
    SECRET_KEY = os.getenv("SECRET_KEY", "")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./library.db")
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "").strip().lower()
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")
    MAX_UPLOAD_BYTES = 20 * 1024 * 1024
    TOKEN_MAX_AGE_SECONDS = 60 * 60 * 24 * 7

settings = Settings()

if settings.DATABASE_URL.startswith("postgres://"):
    settings.DATABASE_URL = settings.DATABASE_URL.replace("postgres://", "postgresql://", 1)
