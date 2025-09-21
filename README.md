# TelegramTrader Bot

A Telegram bot for monitoring trading signals in groups and channels,
then posting them for subscribers to MetaTrader.

## Requirements

- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Docker and Docker Compose (containerized deployment)

## Deployment

The bot can be deployed using `docker-compose` and configured via `.env` file.
Define the following environment variables in a `.env` file:

```sh
# Get from @BotFather
TELEGRAM_BOT_TOKEN=your_bot_token_here
# User ID of admin who owns the bot
ADMIN_USER_ID=123456789
# Production webhook base URL (optional)
WEBHOOK_BASE=your-domain.com
# Production webhook port (optional)
WEBHOOK_PORT=8443
```

See `.env.example` for all available configuration options. Place the file
in the same directory as `docker-compose.yml` (example provided in repo).
Then run the following commands from the directory:

```sh
# Pull latest image and start container
docker-compose pull
docker-compose up -d
```

## Development

Development environment can be configured by defining env vars in `.env` file.
See `.env.example` for all available configuration options.
The following are available scripts for development and maintenance:

```sh
./scripts/app       # Bot app entry point
./scripts/setup.sh  # Setup app environment
./scripts/deploy.sh # Build and push Docker image
./scripts/test.sh   # Test connection to Docker image locally
```

For testing webhooks in development, Tailscale can be used to expose the local
server to the internet. The webhook port can be exposed using:

```sh
tailscale funnel $WEBHOOK_PORT
# > Available on the internet:
# > https://$WEBHOOK_BASE/
# > |-- proxy http://127.0.0.1:$WEBHOOK_PORT
# > Press Ctrl+C to exit.
```

Also, VSCode can forward ports using GitHub authentication with the following setup:

- **Port:** `$WEBHOOK_PORT`
- **Forwarded Address:** `https://$WEBHOOK_BASE/`
- **Visibility:** Must be set to "Public"

## Bot Usage

### Commands

- `/start` - Welcome message and introduction
- `/users` - List subscribed users

### Signal Detection

The bot detects trading signals by looking for:

- **Action keywords**: `BUY`, `SELL`, `LONG`, `SHORT`
- **Currency pairs**: `EURUSD`, `GBP/JPY`, etc.
- **Price levels**: `Entry`, `SL` (stop loss), `TP[n]` (take profits)

Example signal formats supported:

```
BUY EURUSD @ 1.0850 SL: 1.0800 TP: 1.0900
LONG BitcoinUSD Entry: 45000 SL: 44000 TP1: 46000 TP2: 47000
SELL GBP/JPY 145.50 Stop Loss: 146.00 Take Profit: 144.50
```
