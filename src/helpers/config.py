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

    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str

    OPENAI_API_KEY: str = None
    OPENAI_API_URL: str = None
    COHERE_API_KEY: str = None
    ANTHROPIC_API_KEY: str = None
    
    GENERATION_MODEL_ID: str = None
    EMBEDDING_MODEL_ID: str = None
    EMBEDDING_MODEL_SIZE: int = None
    INPUT_DEFAULT_MAX_CHARACTERS: int = None
    GENERATION_DEFAULT_MAX_TOKENS: int = None
    GENERATION_DEFAULT_TEMPERATURE: float = None

    VECTOR_DB_BACKEND : str
    VECTOR_DB_PATH : str
    VECTOR_DB_DISTANCE_METHOD: str = None
    
    DEFAULT_LANG : str
    PRIMARY_LANG : str
    class Config:
        env_file = ".env"

def get_settings():
    return Settings()
    