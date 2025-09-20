__all__ = [
    "Settings",
    "DatabaseException",
    "TelegramException",
]

from pathlib import Path

import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=dotenv.find_dotenv(), extra="allow"
    )

    data_path: Path = Path(__file__).parent.parent / "data"
    telegram_bot_token: str = ""
    database_url: str = f"sqlite:///{data_path/'db.sql'}"


# MARK: Exceptions ============================================================


class DatabaseException(Exception):
    """An exception raised by the database."""

class TelegramException(Exception):
    """An exception raised by the Telegram API."""
