"""
Configurações da Aplicação
===========================

Gerencia todas as configurações através de variáveis de ambiente.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Configurações principais da aplicação"""
    
    # App
    APP_NAME: str = "PyStep"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Servidor
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "sqlite:///./pystep.db"
    
    # Segurança
    SECRET_KEY: str = "your-secret-key-change-this"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    
    # Sandbox
    EXECUTION_TIMEOUT: int = 2
    MAX_MEMORY_MB: int = 128
    ALLOWED_IMPORTS: str = "math,random,datetime,json"
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Converte string de CORS_ORIGINS em lista"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
