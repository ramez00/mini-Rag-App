from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str

    FILE_ALLOWED_EXTENSIONS: list
    FILE_MAX_SIZE: int
    UPLOAD_DIRECTORY: str
    FILE_DEFAULT_CHUNK_SIZE: int
    MONGO_URI: str
    MONGO_DB_NAME: str

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()
    