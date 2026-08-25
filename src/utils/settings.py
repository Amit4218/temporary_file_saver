import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MAX_FILE_SIZE:int = 25 * 1024 * 1024
    HOST_URL:str = os.getenv("HOST_URL") or ""
    DATABASE_URL:str = os.getenv("DATABASE_URL") or ""
    CLOUDINARY_CLOUD_NAME:str = os.getenv("CLOUDINARY_CLOUD_NAME") or ""
    CLOUDINARY_API_KEY:str = os.getenv("CLOUDINARY_API_KEY") or ""
    CLOUDINARY_API_SECRET:str = os.getenv("CLOUDINARY_API_SECRET") or ""

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
