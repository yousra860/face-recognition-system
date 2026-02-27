from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Face Recognition Cloud System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    FACE_TOLERANCE: float = 0.6
    FACE_DETECTION_MODEL: str = "hog"
    DATABASE_URL: str = "sqlite:///./data/face_recognition.db"
    UPLOAD_DIR: str = "./data/faces"
    
    # JWT Settings - إضافة جديدة
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
 DATABASE_URL: str = "sqlite:///./data/face_recognition.db"
    
@property
    def get_database_url(self):
        import os
        return os.getenv("DATABASE_URL", self.DATABASE_URL)
