"""Main entry point for the bot."""

import asyncio
import logging
from typing import Annotated

import typer

from bot.logging import setup_logging
from bot import models

from . import APP_NAME

# setup bot
logger = logging.getLogger(__name__)
app = typer.Typer(
    name=APP_NAME,
    context_settings={"help_option_names": ["-h", "--help"]},
)


@app.callback()
def main(
    debug_mode: Annotated[
        bool,
        typer.Option(
            "--debug", "-d", help="Enable debug mode."
        ),
    ] = False,
) -> None:
    """Main entry point for the bot package."""
    app_settings = models.Settings()
    setup_logging(debug_mode, app_settings.data_path / "bot.log")


@app.command()
def start() -> None:
    """Start the bots."""
    print("running bot...")
    asyncio.run(asyncio.Event().wait())
