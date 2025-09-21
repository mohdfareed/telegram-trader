"""Bot main entry point."""

__all__ = ["app"]

import logging
from typing import Annotated

import typer
from rich import print

from app import APP_NAME, bot, models, server, utils
from app.database import db_session, init_db
from app.database.models import AppMeta

# setup bot
logger = logging.getLogger(__name__)
app = typer.Typer(
    name=APP_NAME,
    help="TelegramTrader bot command line interface.",
    add_completion=False,
)


@app.callback()
def main(
    debug_mode: Annotated[
        bool,
        typer.Option("--debug", "-d", help="Enable debug mode."),
    ] = False,
) -> None:
    """Main entry point for the bot package."""
    settings = models.Settings()
    debug_mode = debug_mode or settings.debug_mode
    utils.setup_logging(debug_mode, settings.logging_file)

    logger.debug("debug mode enabled")
    logger.debug(f"app version: {utils.APP_NAME} {utils.__version__}")
    logger.debug(f"data path: {settings.data_path.absolute()}")


@app.command()
def start() -> None:
    """Start the Telegram bot."""
    settings = models.Settings()
    init_db()
    with db_session() as session:
        AppMeta.load(session)

    try:
        logger.info("running bot...")
        server.start(settings)
        bot.start(settings)
    except KeyboardInterrupt:
        print()
        logger.info("bot stopped")


@app.command()
def health() -> None:
    """Health check command for container probes."""
    settings = models.Settings()

    if pid := server.check(settings):
        logger.info(f"bot is running with PID: {pid}")
        raise typer.Exit(0)

    logger.info("bot is not running")
    raise typer.Exit(1)


@app.command()
def settings() -> None:
    """Display the app settings."""
    app_settings = models.Settings()
    print(app_settings)


@app.command()
def app_info() -> None:
    """Display database AppMeta info."""
    init_db()
    with db_session() as session:
        meta = AppMeta.load(session)
        print(meta)
