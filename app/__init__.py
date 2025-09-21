"""TelegramTrader Bot.

A Telegram bot for posting trading signals using MetaTrader.
"""

import subprocess

APP_NAME, __version__ = (
    subprocess.run(["uv", "version"], capture_output=True, text=True, check=True)
    .stdout.strip()
    .split()
)
