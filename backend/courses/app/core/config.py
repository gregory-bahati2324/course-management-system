from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"
    USER_SERVICE_DB_URL: str = "sqlite:///./user_service.db"
    
    SECRET_KEY : str = "super-secret-key"
    AUTH_SERVICE_URL: str = "http://127.0.0.1:8000"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    class config:
        env_file = ".env"
        
settings = Settings()
