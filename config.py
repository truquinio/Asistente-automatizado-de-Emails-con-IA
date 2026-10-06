from enum import Enum

from pydantic import EmailStr, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class EmailCategory(str, Enum):
    SUPPORT = "soporte"
    SALES = "ventas"
    INQUIRY = "consulta"
    SPAM = "spam"
    OTHER = "otro"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4.1-mini"
    OPENAI_TEMPERATURE: float = 0.7
    OPENAI_MAX_TOKENS: int = 500
    OPENAI_TIMEOUT: int = 30

    IMAP_SERVER: str = "imap.gmail.com"
    IMAP_PORT: int = 993
    EMAIL_ACCOUNT: EmailStr
    EMAIL_PASSWORD: str
    EMAIL_FOLDERS: list[str] = Field(default_factory=lambda: ["INBOX", "Important"])

    PROCESSING_LIMIT: int = 10
    PROCESSING_INTERVAL: int = 300
    MAX_EMAIL_SIZE: int = 1024 * 1024

    DEFAULT_TIMEZONE: str = "Europe/Madrid"
    COMPANY_NAME: str = "Mi Empresa"
    SUPPORT_EMAIL: EmailStr = "soporte@miempresa.com"

    ALLOWED_DOMAINS: list[str] = Field(default_factory=lambda: ["gmail.com", "miempresa.com"])
    BLACKLIST: list[str] = Field(default_factory=list)

    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "email_assistant.log"
    LOG_ROTATION: str = "10 MB"

    @field_validator("OPENAI_TEMPERATURE")
    @classmethod
    def validate_temperature(cls, value: float) -> float:
        if not 0 <= value <= 1:
            raise ValueError("La temperatura debe estar entre 0 y 1")
        return value

    @field_validator("IMAP_PORT")
    @classmethod
    def validate_port(cls, value: int) -> int:
        if not 1 <= value <= 65535:
            raise ValueError("Puerto IMAP inválido")
        return value

    @field_validator("PROCESSING_LIMIT")
    @classmethod
    def validate_limit(cls, value: int) -> int:
        if value < 1:
            raise ValueError("El límite debe ser al menos 1")
        return min(value, 50)


config = Settings()
