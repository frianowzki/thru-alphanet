# Thru Alphanet Telegram Bot

Telegram bot untuk interact sama Thru blockchain.

## Setup

1. Buat bot via @BotFather di Telegram
2. Set environment variable:
```bash
export THRU_BOT_TOKEN="your-token-here"
```

3. Run:
```bash
python3 bot.py
```

## Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message |
| `/balance [address]` | Check balance |
| `/send <to> <amount>` | Send tokens |
| `/deploy <binary> [seed]` | Deploy program |
| `/programs` | List recent programs |
| `/status` | Network status |
| `/help` | Show help |

## Requirements

- Python 3.10+
- `python-telegram-bot`
- `thru` CLI installed and configured
