"""Telegram bot startup and handlers."""

import logging
import secrets
from typing import Final, NoReturn

import telegram
import telegram.ext as telegram_ext

from app import models

logger = logging.getLogger(__name__)


def start(settings: models.Settings) -> None:
    """Build and run the Telegram bot."""

    # get the bot token
    token: Final[str] = settings.telegram_bot_token
    if not token:
        raise models.TelegramException("TELEGRAM_BOT_TOKEN is not configured.")

    # configure the bot
    defaults = telegram_ext.Defaults(
        parse_mode=telegram.constants.ParseMode.HTML,
        allow_sending_without_reply=True,
        block=False,
    )

    app = (  # create the application
        telegram_ext.Application.builder()
        .token(token)
        .rate_limiter(telegram_ext.AIORateLimiter())
        .defaults(defaults)
        .build()
    )

    # register handlers
    app.add_handler(_create_log_handler(), group=-1)
    app.add_error_handler(_error_handler)

    # check if webhook is configured
    if settings.webhook_port > 0:
        url = f"https://{settings.webhook_base}/{settings.webhook_path}"
        logger.info(f"starting webhook on: 0.0.0.0:{settings.webhook_port} -> {url}")

        # run in production mode
        app.run_webhook(
            listen="0.0.0.0",
            port=settings.webhook_port,
            webhook_url=url,
            url_path=settings.webhook_path,
            secret_token=secrets.token_hex(32),
            drop_pending_updates=True,
        )

    else:  # run in polling mode
        logger.info("running in polling mode")
        app.run_polling(drop_pending_updates=True)
    raise KeyboardInterrupt  # gracefully stop app


def _create_log_handler() -> telegram_ext.TypeHandler[
    telegram.Update, telegram_ext.ContextTypes.DEFAULT_TYPE, None
]:
    async def log(update: telegram.Update) -> None:
        logger.debug(f"received update: {update}")

    return telegram_ext.TypeHandler(
        telegram.Update, lambda update, _: log(update), block=False
    )


async def _error_handler(
    update: object, context: telegram_ext.ContextTypes.DEFAULT_TYPE
) -> NoReturn:
    # reply with the error message if possible
    if isinstance(update, telegram.Update) and update.effective_message:
        reply = f"<code>{str(context.error)}</code>"
        await update.effective_message.reply_html(reply)

    # re-raise the error to be logged
    raise context.error or models.TelegramException("unknown error encountered...")
