"""Bot main entry point."""

__all__ = ["app"]

import logging
from typing import Annotated

import typer
from rich import print

from app import bot, models, utils
from app.database import db_session, init_db
from app.database.models import AppMeta

# setup bot
logger = logging.getLogger(__name__)
app = typer.Typer(
    name=utils.__app__,
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
    logger.debug(f"app version: {utils.__app__} {utils.__version__}")
    logger.debug(f"data path: {settings.data_path}")

    init_db()
    with db_session() as session:
        AppMeta.load(session)


@app.command()
def start() -> None:
    """Start the Telegram bot."""
    settings = models.Settings()
    utils.track_bot(settings.data_path)

    try:
        logger.info("running bot...")
        bot.start(settings)
    except KeyboardInterrupt:
        print()
        logger.info("bot stopped")


@app.command()
def health() -> None:
    """Health check command for container probes."""
    settings = models.Settings()

    if pid := utils.is_healthy(settings.data_path):
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
    with db_session() as session:
        meta = AppMeta.load(session)
        print(meta)


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
