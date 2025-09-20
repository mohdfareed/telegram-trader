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
    settings = models.Settings()
    utils.setup_logging(debug_mode, settings.data_path / "bot.log")

    logger.debug("debug mode enabled.")
    logger.debug(f"data path: {settings.data_path}")


@app.command()
def start() -> None:
    """Start the Telegram bot."""
    settings = models.Settings()
    settings = settings  # TODO: remove when bot is implemented

    try:
        logger.info("running bot...")
        # TODO: implement and start bot
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
