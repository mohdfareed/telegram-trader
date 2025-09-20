"""Main entry point for the bot."""

import asyncio
import logging
from typing import Annotated

import typer

from bot import models, utils

from . import APP_NAME

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
    print("running bot...")
    asyncio.run(asyncio.Event().wait())
