"""Bot utilities."""

__all__ = ["setup_logging", "__app__", "__version__"]

import atexit
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

from rich.logging import RichHandler
from rich.text import Text

from app import __app__, __version__
from app.models import ApplicationException

HEALTH_FILE = Path("bot.pid")
"""Health check file path."""

WARN_MODULES = ["asyncio", "telegram", "telegram.ext", "httpcore", "httpx"]
"""Modules for which to log warnings and above."""


def setup_logging(debug: bool, log_file: Path) -> None:
    """Setup logging for the application."""
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.NOTSET)

    root_logger.addHandler(_console_handler(debug))
    root_logger.addHandler(_file_handler(log_file))

    for module in WARN_MODULES:  # Reduce log level for non-debug modules
        logging.getLogger(module).setLevel(logging.WARNING)


def track_bot(data_path: Path) -> None:
    """Start tracking the health of the bot."""
    health_file = data_path / HEALTH_FILE
    health_file.parent.mkdir(parents=True, exist_ok=True)

    # check if health file path exists
    if health_file.exists():
        raise ApplicationException(f"bot is already running: {health_file.read_text()}")

    # create file and delete on exit
    health_file.write_text(str(os.getpid()))
    atexit.register(lambda: health_file.unlink(missing_ok=True))


def is_healthy(data_path: Path) -> str | None:
    """Check if the bot is healthy, return the PID if it is."""
    health_file = data_path / HEALTH_FILE
    return health_file.read_text() if health_file.exists() else None


def _console_handler(debug: bool) -> logging.Handler:
    handler = RichHandler(markup=True, show_path=False)
    handler.setFormatter(logging.Formatter(r"%(message)s [bright_black]\[%(name)s][/]"))
    handler.setLevel(logging.DEBUG if debug else logging.INFO)
    return handler


def _file_handler(log_file: Path) -> logging.Handler:
    class _StripMarkupFilter(logging.Filter):
        def filter(self, record: logging.LogRecord) -> bool:
            if hasattr(record, "msg") and isinstance(record.msg, str):
                record.msg = Text.from_markup(Text.from_ansi(record.msg).plain).plain
            return True  # filter rich markup and ansi escape codes

    # ensure log file and parent directories exist
    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.touch(exist_ok=True)

    # add a header to the log file
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    file_header = f"[{timestamp}]" + "=" * (80 - 2 - len(timestamp) - 1)
    with open(log_file, "a") as file:
        file.write(file_header + "\n")

    # create rotating file handler
    file = RotatingFileHandler(log_file, maxBytes=2**20, backupCount=5, delay=True)

    # configure file handler
    file.addFilter(_StripMarkupFilter())
    file.setLevel(logging.NOTSET)
    file.setFormatter(
        logging.Formatter(
            r"[%(asctime)s.%(msecs)03d] %(levelname)-8s %(message)s [%(name)s@%(filename)s:%(lineno)d]",
            datefmt=r"%Y-%m-%d %H:%M:%S",
        )
    )
    return file
