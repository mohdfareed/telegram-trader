"""TelegramTrader Bot.

A Telegram bot for posting trading signals using MetaTrader.
"""

import subprocess

__app__, __version__ = (
    subprocess.run(["uv", "version"], capture_output=True, text=True, check=True)
    .stdout.strip()
    .split()
)
