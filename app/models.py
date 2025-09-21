"""Bot models and settings."""

__all__ = [
    "Settings",
    "ApplicationException",
    "DatabaseException",
    "TelegramException",
]

from pathlib import Path

import dotenv
import typer
from pydantic_settings import BaseSettings, SettingsConfigDict

from app import APP_NAME


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=dotenv.find_dotenv(), extra="allow")

    data_path: Path = Path(typer.get_app_dir(APP_NAME))
    debug_mode: bool = False

    telegram_bot_token: str = ""
    database_url: str = f"sqlite:///{data_path / 'database.sql'}"

    webhook_port: int = 0
    webhook_base: str = ""
    webhook_path: str = ""


# MARK: Exceptions ============================================================


class ApplicationException(Exception):
    """A general application exception."""


class DatabaseException(ApplicationException):
    """An exception raised by the database."""


class TelegramException(ApplicationException):
    """An exception raised by the Telegram API."""
