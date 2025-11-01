from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


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
    
    def _split_origins(self, value: str) -> List[str]:
        if not value:
            return []
        return [origin.strip() for origin in value.split(",") if origin.strip()]

    def _normalize_origin(self, origin: str) -> str:
        return origin.rstrip("/")

    def get_cors_origins(self) -> List[str]:
        """Get all allowed CORS origins"""
        raw_origins: List[str] = []

        # Primary frontend URLs (support comma-separated values)
        raw_origins.extend(self._split_origins(self.FRONTEND_URL))

        # Default development origins
        raw_origins.extend([
            "http://localhost:3000",
            "http://localhost:5173",
            "http://localhost:5174",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
        ])

        # Production defaults (Vercel deployment)
        raw_origins.extend([
            "https://hospitalsystem001.vercel.app",
        ])

        # Additional origins from environment
        raw_origins.extend(self._split_origins(self.ALLOWED_ORIGINS))

        # Normalize and deduplicate while preserving order
        normalized: List[str] = []
        seen = set()
        for origin in raw_origins:
            if not origin:
                continue
            cleaned = self._normalize_origin(origin)
            if cleaned not in seen:
                seen.add(cleaned)
                normalized.append(cleaned)

        return normalized


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()

