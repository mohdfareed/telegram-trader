"""SQLModel engine and session utilities."""

from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import Generator, Optional

from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine

from app import models as app_models

logger = logging.getLogger(__name__)


_engine: Engine | None = None


def init_db() -> None:
    """Initialize database engine and create tables."""
    engine = _get_engine()
    logger.debug("creating database tables...")
    SQLModel.metadata.create_all(engine)


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

    settings = app_models.Settings()
    url = database_url or settings.database_url

    # sqlite needs check_same_thread=False to work across threads in some cases
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}

    _engine = create_engine(url, echo=settings.debug_mode, connect_args=connect_args)
    logger.info(f"database engine created: {url}")
    return _engine
