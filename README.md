# TelegramTrader Bot

A Telegram bot for monitoring trading signals in groups and channels,
then posting them for subscribers to MetaTrader.

## Requirements

- Python 3.13 or higher
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Docker and Docker Compose (containerized deployment)

## Deployment

Define the following environment variables:

```sh
# Get from @BotFather
TELEGRAM_BOT_TOKEN=your_bot_token_here
# User ID of admin who owns the bot
ADMIN_USER_ID=123456789
# Production webhook URL
WEBHOOK_URL=https://yourdomain.com/webhook
```

See `.env.example` for all available configuration options.

Then clone the repository and deploy the bot using:

```sh
# pull repo to get docker-compose.yml and .env.example
git clone https://github.com/mohdfareed/telegram-trader.git
cd telegram-trader

# pull latest image and start container
docker-compose pull
docker-compose up -d
```

## Development

Development environment can be configured by defining env vars in `.env` file.
See `.env.example` for all available configuration options.
The following are available scripts for development and maintenance:

```sh
./scripts/setup.sh  # Setup development environment
./scripts/start.sh  # Run bot in development mode
./scripts/deploy.sh # Run bot in production mode
./scripts/update.sh # Update project dependencies
```

## Signal Detection

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

## Bot Commands

### User Commands

- `/start` - Welcome message and introduction

### Admin Commands

- `/users` - List subscribed users
