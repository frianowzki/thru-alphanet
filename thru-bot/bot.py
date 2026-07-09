#!/usr/bin/env python3
"""Thru Alphanet Telegram Bot — Check balance, send tokens, deploy programs"""

import os
import subprocess
import json
import logging
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Config
BOT_TOKEN = os.environ.get("THRU_BOT_TOKEN", "")
RPC_URL = "https://rpc.alphanet.thru.org"
FEE_PAYER = os.environ.get("THRU_KEY_NAME", "default")  # key name in ~/.thru/cli/config.yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def thru_cmd(args: list[str], timeout: int = 30) -> dict:
    """Execute thru CLI command and return JSON output."""
    cmd = ["thru", "--json"] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if result.stdout.strip():
            return json.loads(result.stdout)
        return {"error": result.stderr or "No output"}
    except subprocess.TimeoutExpired:
        return {"error": "Command timed out"}
    except json.JSONDecodeError:
        return {"error": f"Invalid JSON: {result.stdout[:200]}"}
    except Exception as e:
        return {"error": str(e)}


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message."""
    await update.message.reply_text(
        "🕊️ **Thru Alphanet Bot**\n\n"
        "Commands:\n"
        "/balance `<address>` — Check balance\n"
        "/send `<to> <amount>` — Send tokens\n"
        "/deploy `<binary_path>` — Deploy program\n"
        "/programs — List deployed programs\n"
        "/status — Network status\n"
        "/help — Show this message",
        parse_mode="Markdown"
    )


async def cmd_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check account balance."""
    if not context.args:
        # Default key name from env or config
        data = thru_cmd(["account", "info", FEE_PAYER])
        if "account_info" in data:
            info = data["account_info"]
            await update.message.reply_text(
                f"💰 **Balance**\n"
                f"Address: `{info.get('address', 'N/A')}`\n"
                f"Balance: {info.get('balance', 0):,} tokens",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(f"❌ Error: {json.dumps(data)[:200]}")
        return

    address = context.args[0]
    data = thru_cmd(["account", "info", address])
    if "account_info" in data:
        info = data["account_info"]
        await update.message.reply_text(
            f"💰 **Balance**\n"
            f"Address: `{info.get('address', address)}`\n"
            f"Balance: {info.get('balance', 0):,} tokens",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(f"❌ Error: {json.dumps(data)[:200]}")


async def cmd_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send tokens."""
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /send `<to_address> <amount>`", parse_mode="Markdown")
        return

    to_addr = context.args[0]
    amount = context.args[1]

    data = thru_cmd(["transfer", FEE_PAYER, to_addr, amount, "--json"])
    if "transfer" in data and data["transfer"].get("status") == "success":
        sig = data["transfer"].get("signature", "N/A")[:20]
        await update.message.reply_text(
            f"✅ **Transfer Sent**\n"
            f"To: `{to_addr}`\n"
            f"Amount: {amount} tokens\n"
            f"Sig: `{sig}...`",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(f"❌ Transfer failed: {json.dumps(data)[:200]}")


async def cmd_deploy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Deploy a program."""
    if not context.args:
        await update.message.reply_text("Usage: /deploy `<binary_path> [seed]`", parse_mode="Markdown")
        return

    binary_path = context.args[0]
    seed = context.args[1] if len(context.args) > 1 else f"bot-{int(__import__('time').time())}"

    if not os.path.exists(binary_path):
        await update.message.reply_text(f"❌ File not found: {binary_path}")
        return

    await update.message.reply_text(f"🚀 Deploying `{binary_path}` as `{seed}`...")

    data = thru_cmd(["program", "create", seed, binary_path, "--authority", FEE_PAYER], timeout=60)
    if "program_create" in data and data["program_create"].get("status") == "success":
        info = data["program_create"]
        await update.message.reply_text(
            f"✅ **Program Deployed!**\n"
            f"Seed: `{info['seed']}`\n"
            f"Program: `{info['program_account']}`\n"
            f"Meta: `{info['meta_account']}`\n"
            f"Size: {info['program_size']} bytes",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(f"❌ Deploy failed: {json.dumps(data)[:300]}")


async def cmd_programs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List recent programs."""
    data = thru_cmd(["program", "list", "--limit", "5"])
    if "programs" in data:
        lines = ["📦 **Recent Programs**\n"]
        for prog in data["programs"][:5]:
            lines.append(f"• `{prog.get('address', 'N/A')[:20]}...` — {prog.get('size', 0)} bytes")
        await update.message.reply_text("\n".join(lines), parse_mode="Markdown")
    else:
        # Fallback: just show status
        await update.message.reply_text("📦 Program list not available. Use /deploy to create one.")


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Network status."""
    height_data = thru_cmd(["getheight"])
    health_data = thru_cmd(["gethealth"])

    height = height_data.get("height", "N/A") if "height" in height_data else "N/A"
    health = health_data.get("health", "N/A") if "health" in health_data else "N/A"

    await update.message.reply_text(
        f"🌐 **Thru Alphanet Status**\n"
        f"Height: {height}\n"
        f"Health: {health}\n"
        f"RPC: `{RPC_URL}`",
        parse_mode="Markdown"
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help."""
    await cmd_start(update, context)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle unknown messages."""
    await update.message.reply_text(
        "🤔 Unknown command. Use /help to see available commands."
    )


def main():
    if not BOT_TOKEN:
        print("Error: Set THRU_BOT_TOKEN environment variable")
        print("  export THRU_BOT_TOKEN='your-telegram-bot-token'")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    # Register commands
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("balance", cmd_balance))
    app.add_handler(CommandHandler("send", cmd_send))
    app.add_handler(CommandHandler("deploy", cmd_deploy))
    app.add_handler(CommandHandler("programs", cmd_programs))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Set bot commands
    async def post_init(application: Application):
        await application.bot.set_my_commands([
            BotCommand("start", "Start the bot"),
            BotCommand("balance", "Check balance"),
            BotCommand("send", "Send tokens"),
            BotCommand("deploy", "Deploy program"),
            BotCommand("programs", "List programs"),
            BotCommand("status", "Network status"),
            BotCommand("help", "Show help"),
        ])

    app.post_init = post_init

    print("🤖 Thru Bot starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
