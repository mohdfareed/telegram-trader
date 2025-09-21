"""Bot models and settings."""

__all__ = [
    "Settings",
    "ApplicationException",
    "DatabaseException",
    "TelegramException",
]

import os
from pathlib import Path

import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

from app import APP_NAME


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=dotenv.find_dotenv(), extra="allow")

    data_path: Path = Path(__file__).parent.parent / "data"
    logging_file: Path = data_path / "bot.log"
    debug_mode: bool = False

    telegram_bot_token: str = ""
    database_url: str = f"sqlite:///{data_path.absolute() / 'bot.sql'}"
    server_port: int = 8081

    webhook_port: int = 0
    webhook_base: str = ""
    webhook_path: str = APP_NAME


# MARK: Exceptions ============================================================


class ApplicationException(Exception):
    """A general application exception."""


class DatabaseException(ApplicationException):
    """An exception raised by the database."""


class TelegramException(ApplicationException):
    """An exception raised by the Telegram API."""


# MARK: Fix Settings Dependencies =============================================

settings = Settings()
os.environ["LOGGING_FILE"] = f"{settings.data_path.absolute() / 'bot.log'}"
os.environ["DATABASE_URL"] = f"sqlite:///{settings.data_path.absolute() / 'bot.sql'}"
