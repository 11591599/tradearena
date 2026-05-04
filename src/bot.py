"""Telegram bot for TradeArena Mini App."""
import os
import logging
from telegram import Update, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from loguru import logger

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
WEBAPP_URL = os.getenv("WEBHOOK_URL", "https://tradearena.app")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message with WebApp button."""
    keyboard = [
        [KeyboardButton(text="🎮 Play TradeArena", web_app=WebAppInfo(url=WEBAPP_URL))],
        [KeyboardButton(text="🏆 Leaderboard"), KeyboardButton(text="💎 Premium")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "🏆 *TradeArena*\n\n"
        "Compete in crypto trading battles!\n"
        "$10,000 virtual balance. Real prizes.\n\n"
        "🎮 Tap *Play* to start trading!\n"
        "📊 BTC, ETH, SOL — all live prices\n"
        "🏆 Win rounds, climb the leaderboard\n"
        "💎 Premium unlocks more features\n\n"
        "Invite friends and get +20% bonus!",
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )


async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Open the Mini App."""
    keyboard = [
        [KeyboardButton(text="🎮 Play TradeArena", web_app=WebAppInfo(url=WEBAPP_URL))],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "🎮 Open TradeArena and start trading!",
        reply_markup=reply_markup,
    )


async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show top players."""
    import httpx
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"http://localhost:8000/api/leaderboard/global")
            players = resp.json()[:10]

        text = "🏆 *Top Traders*\n\n"
        medals = ["🥇", "🥈", "🥉"]
        for i, p in enumerate(players):
            medal = medals[i] if i < 3 else f"{i+1}."
            text += f"{medal} {p['username']} — {p['pnl']:+.2f} USDT\n"

        if not players:
            text = "🏆 No players yet. Be the first!"

        await update.message.reply_text(text, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Leaderboard error: {e}")
        await update.message.reply_text("Error loading leaderboard. Try again later.")


async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Premium info."""
    await update.message.reply_text(
        "💎 *TradeArena Premium*\n\n"
        "• Extended charts (1m, 5m, 15m)\n"
        "• Priority matching\n"
        "• 5x boosts daily\n"
        "• Premium badge\n"
        "• 20+ trading pairs\n"
        "• Auto stop-loss\n\n"
        "Price: 0.5 TON (lifetime)\n\n"
        "Open the app to purchase!",
        parse_mode="Markdown",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help message."""
    await update.message.reply_text(
        "🏆 *TradeArena Commands*\n\n"
        "/start — Open the game\n"
        "/play — Start trading\n"
        "/leaderboard — Top players\n"
        "/premium — Premium features\n"
        "/help — This message",
        parse_mode="Markdown",
    )


async def setup_bot():
    """Initialize and return bot application."""
    if not BOT_TOKEN:
        logger.warning("TELEGRAM_BOT_TOKEN not set, bot disabled")
        return None

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", play))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(CommandHandler("premium", premium))
    app.add_handler(CommandHandler("help", help_command))

    await app.initialize()
    await app.start()

    webhook_url = f"{WEBAPP_URL}/webhook"
    await app.updater.start_webhook(
        listen="0.0.0.0",
        port=8001,
        url_path="webhook",
        webhook_url=webhook_url,
    )

    logger.info(f"Bot started with webhook: {webhook_url}")
    return app