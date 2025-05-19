import os
from dotenv import load_dotenv
from enum import Enum
from pydantic import BaseSettings, validator, EmailStr
from typing import Optional, List

load_dotenv()

class EmailCategory(str, Enum):
    SUPPORT = "soporte"
    SALES = "ventas"
    INQUIRY = "consulta"
    SPAM = "spam"
    OTHER = "otro"

class Settings(BaseSettings):
    # Configuración OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-3.5-turbo-1106"
    OPENAI_TEMPERATURE: float = 0.7
    OPENAI_MAX_TOKENS: int = 500
    OPENAI_TIMEOUT: int = 30
    
    # Configuración Email
    IMAP_SERVER: str = "imap.gmail.com"
    IMAP_PORT: int = 993
    EMAIL_ACCOUNT: EmailStr
    EMAIL_PASSWORD: str  # Usar App Password si tiene 2FA
    EMAIL_FOLDERS: List[str] = ["INBOX", "Important"]
    
    # Configuración Procesamiento
    PROCESSING_LIMIT: int = 10
    PROCESSING_INTERVAL: int = 300  # segundos
    MAX_EMAIL_SIZE: int = 1024 * 1024  # 1MB
    
    # Configuración Respuestas
    DEFAULT_TIMEZONE: str = "America/Mexico_City"
    COMPANY_NAME: str = "Mi Empresa"
    SUPPORT_EMAIL: EmailStr = "soporte@miempresa.com"
    
    # Configuración Seguridad
    ALLOWED_DOMAINS: List[str] = ["gmail.com", "miempresa.com"]
    BLACKLIST: List[str] = []
    
    # Configuración Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "email_assistant.log"
    LOG_ROTATION: str = "10 MB"
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
    
    @validator('OPENAI_TEMPERATURE')
    def validate_temperature(cls, v):
        if not 0 <= v <= 1:
            raise ValueError("La temperatura debe estar entre 0 y 1")
        return v
    
    @validator('IMAP_PORT')
    def validate_port(cls, v):
        if not 1 <= v <= 65535:
            raise ValueError("Puerto IMAP inválido")
        return v
    
    @validator('PROCESSING_LIMIT')
    def validate_limit(cls, v):
        if v < 1:
            raise ValueError("El límite debe ser al menos 1")
        return min(v, 50)  # Máximo 50 emails por ejecución

# Instancia de configuración global
config = Settings()

# Validación adicional al importar
try:
    config = Settings()
except Exception as e:
    raise RuntimeError(f"Error en configuración: {str(e)}") from e