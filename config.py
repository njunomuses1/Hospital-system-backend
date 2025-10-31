from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/hospital_db"
    DATABASE_SSL: bool = False  # Enable when using managed MySQL that requires TLS (e.g., Railway)
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # CORS - Support multiple frontend URLs (comma-separated)
    FRONTEND_URL: str = "http://localhost:3000"
    ALLOWED_ORIGINS: str = ""  # Additional origins, comma-separated
    
    # Application
    APP_NAME: str = "Hospital Management System"
    VERSION: str = "1.0.0"
    
    # JWT Authentication
    SECRET_KEY: str = "your-super-secret-jwt-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Environment
    ENVIRONMENT: str = "development"  # development, production
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def get_cors_origins(self):
        """Get all allowed CORS origins"""
        origins = [
            self.FRONTEND_URL,
            "http://localhost:3000",
            "http://localhost:5173",
            "http://localhost:5174",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
        ]
        
        # Add additional origins from environment
        if self.ALLOWED_ORIGINS:
            additional = [o.strip() for o in self.ALLOWED_ORIGINS.split(",")]
            origins.extend(additional)
        
        return origins


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()

