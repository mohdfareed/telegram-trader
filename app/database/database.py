"""SQLModel engine and session utilities."""

from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import Generator, Optional

from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine

from app import models

logger = logging.getLogger(__name__)


_engine: Engine | None = None


def init_db() -> None:
    """Initialize database engine and create tables."""
    try:
        engine = _get_engine()
        logger.debug("creating database tables...")
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        raise models.DatabaseException("failed to initialize database") from e


@contextmanager
def db_session() -> Generator[Session, None, None]:
    """Create a new SQLModel session with commit/rollback."""
    session = Session(_get_engine())

    try:
        yield session
        session.commit()
    except Exception:
        logger.error("session errored, rolling back...")
        session.rollback()
        raise
    finally:
        session.close()


def _get_engine(database_url: Optional[str] = None) -> Engine:
    global _engine
    if _engine is not None:
        return _engine

    settings = models.Settings()
    url = database_url or settings.database_url

    try:
        _engine = create_engine(url, echo=settings.debug_mode)
        logger.info(f"database engine created: {url}")
        return _engine
    except Exception as e:
        raise models.DatabaseException("failed to create database engine") from e
