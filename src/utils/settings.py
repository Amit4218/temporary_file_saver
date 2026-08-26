from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MAX_FILE_SIZE: int = 25 * 1024 * 1024
    HOST_URL: str = ""
    DATABASE_URL: str = ""
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()