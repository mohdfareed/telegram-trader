"""Database models using SQLModel."""

from __future__ import annotations

import logging
from datetime import datetime

from sqlmodel import Field, Session, SQLModel, select

from app import utils


class AppMeta(SQLModel, table=True):
    """Singleton app metadata row with basic info and timestamps."""

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(default="bot", index=True)
    version: str = Field(default="0.0.0")
    created_at: datetime = Field(default_factory=lambda: datetime.now())

    @staticmethod
    def load(session: Session) -> AppMeta:
        """Fetch or update the current AppMeta row."""
        current = AppMeta(name=utils.APP_NAME, version=utils.__version__)
        rows = session.exec(statement=select(AppMeta)).all()
        last = sorted(rows, key=lambda r: r.created_at)[-1] if rows else None

        # create or update if app version changed
        if last is None or current.version != last.version:
            logger = logging.getLogger(AppMeta.__name__)
            logger.info(f"updating app meta: {current.version}")

            last = current
            session.add(last)
            session.commit()
            session.refresh(last)
        return last
