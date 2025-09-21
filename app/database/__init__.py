"""Database package.

Provides a minimal SQLModel setup with:
- Engine creation from app settings
- Database initialization (create tables)
- Session context manager with commit/rollback and logging
"""

__all__ = ["init_db", "db_session", "models"]

from . import models
from .database import db_session, init_db
