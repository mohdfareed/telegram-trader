"""Bot main entry point."""

import asyncio
import logging
from typing import Annotated

import typer
from rich import print

from app import APP_NAME, models, utils

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
    app_settings = models.Settings()
    utils.setup_logging(debug_mode, app_settings.data_path / "bot.log")


@app.command()
def start() -> None:
    """Start the Telegram bot."""
    try:
        logger.info("running bot...")
        asyncio.run(asyncio.Event().wait())
    except KeyboardInterrupt:
        print()
        logger.info("bot stopped.")


@app.command()
def settings() -> None:
    """Display the app settings."""
    app_settings = models.Settings()
    logger.debug(f"app settings: {app_settings.model_dump_json(indent=2)}")
    print(app_settings)
