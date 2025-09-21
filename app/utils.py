"""Bot utilities."""

__all__ = ["setup_logging", "APP_NAME", "__version__"]

import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

from rich.logging import RichHandler
from rich.text import Text

from app import APP_NAME, __version__

WARN_MODULES = ["asyncio", "telegram", "telegram.ext", "httpcore", "httpx"]
"""Modules for which to log warnings and above."""


def setup_logging(debug: bool, log_file: Path) -> None:
    """Setup logging for the application."""
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.NOTSET)

    level = logging.DEBUG if debug else logging.INFO
    root_logger.addHandler(_console_handler(level))
    root_logger.addHandler(_file_handler(level, log_file))

    for module in WARN_MODULES:  # Reduce log level for non-debug modules
        logging.getLogger(module).setLevel(logging.WARNING)


def _console_handler(level: int) -> logging.Handler:
    handler = RichHandler(markup=True, show_path=False)
    handler.setFormatter(logging.Formatter(r"%(message)s [bright_black]\[%(name)s][/]"))
    handler.setLevel(level)
    return handler


def _file_handler(level: int, log_file: Path) -> logging.Handler:
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
    file.setLevel(level)
    file.setFormatter(
        logging.Formatter(
            r"[%(asctime)s.%(msecs)03d] %(levelname)-8s | %(message)s [%(name)s@%(filename)s:%(lineno)d]",
            datefmt=r"%Y-%m-%d %H:%M:%S",
        )
    )
    return file
