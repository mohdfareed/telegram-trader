"""Bot main entry point."""

__all__ = ["app"]

import logging
from typing import Annotated

import typer
from rich import print

from app import APP_NAME, bot, models, utils

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
    utils.setup_logging(debug_mode, settings.data_path / "bot.log")

    logger.debug("debug mode enabled")
    logger.debug(f"data path: {settings.data_path}")


@app.command()
def start() -> None:
    """Start the Telegram bot."""
    settings = models.Settings()

    try:
        logger.info("running bot...")
        bot.start(settings)
    except KeyboardInterrupt:
        print()
        logger.info("bot stopped")


@app.command()
def settings() -> None:
    """Display the app settings."""
    app_settings = models.Settings()
    logger.debug(f"app settings: {app_settings.model_dump_json(indent=2)}")
    print(app_settings)


@app.command()
def test_server() -> None:
    """Start a simple HTTP server for port testing."""
    import http.server
    import socketserver

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            address = self.client_address[0]
            logger.info(f"GET {self.path} from {address}")

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

        def do_POST(self) -> None:
            address = self.client_address[0]
            body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            logger.info(f"POST {self.path} from {address}: {body.decode()}")

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"RECEIVED")

        def log_message(self, format: str, *args: object) -> None:
            return

    settings = models.Settings()
    webhook_url = f"0.0.0.0:{settings.webhook_port}"
    logger.info(f"starting test server on: {webhook_url}")

    try:
        url = ("0.0.0.0", settings.webhook_port)
        with socketserver.TCPServer(url, Handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print()
        logger.info("server stopped")
