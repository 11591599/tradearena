"""Telegram bot lifecycle and commands for TradeArena."""
import os
from urllib.parse import urlparse

import httpx
from loguru import logger
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    Update,
    WebAppInfo,
)
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
WEBAPP_URL = os.getenv("WEBAPP_URL", "").strip()
API_BASE_URL = os.getenv("INTERNAL_API_URL", "http://127.0.0.1:8000/api").rstrip("/")


def _validate_configuration() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is required. Set it in the server environment.")
    parsed = urlparse(WEBAPP_URL)
    if parsed.scheme != "https" or not parsed.netloc:
        raise RuntimeError("WEBAPP_URL must be the public HTTPS address of the deployed Mini App.")


def _play_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [[KeyboardButton(text="🎮 Open TradeArena", web_app=WebAppInfo(url=WEBAPP_URL))]],
        resize_keyboard=True,
        is_persistent=True,
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_message:
        return
    await update.effective_message.reply_text(
        "🌌 *TradeArena — enter the arena*\n\n"
        "Trade with virtual funds, complete missions, collect tickets and challenge other players.\n\n"
        "Tap below to open the secure Telegram Mini App.\n"
        "Your Telegram account is verified when the app opens.",
        parse_mode="Markdown",
        reply_markup=_play_keyboard(),
    )


async def play(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message:
        await update.effective_message.reply_text(
            "Ready when you are. Open the arena below:", reply_markup=_play_keyboard()
        )


async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_message:
        return
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.get(f"{API_BASE_URL}/leaderboard/global")
            response.raise_for_status()
            payload = response.json()
        players = payload.get("leaderboard", payload) if isinstance(payload, dict) else payload
        if not isinstance(players, list):
            raise ValueError("Unexpected leaderboard response")
        lines = ["🏆 *Arena leaderboard*", ""]
        medals = ["🥇", "🥈", "🥉"]
        for index, player in enumerate(players[:10]):
            name = str(player.get("username") or "Trader").replace("[", "\\[")
            pnl = float(player.get("pnl", 0))
            lines.append(f"{medals[index] if index < 3 else f'{index + 1}.'} {name} — {pnl:+.2f}")
        if not players:
            lines.append("No traders yet. Be the first to enter the arena!")
        await update.effective_message.reply_text("\n".join(lines), parse_mode="Markdown")
    except (httpx.HTTPError, ValueError, TypeError) as exc:
        logger.warning("Could not load leaderboard: {}", exc)
        await update.effective_message.reply_text("Leaderboard is temporarily unavailable. Try again soon.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message:
        await update.effective_message.reply_text(
            "🌌 *TradeArena commands*\n\n"
            "/start — open the arena\n"
            "/play — open the Mini App\n"
            "/leaderboard — top traders\n"
            "/help — show this help",
            parse_mode="Markdown",
            reply_markup=_play_keyboard(),
        )


async def setup_bot() -> Application | None:
    """Validate settings, verify bot token with Telegram, and start long polling."""
    if not BOT_TOKEN:
        logger.warning("TELEGRAM_BOT_TOKEN is not set; Telegram bot is disabled.")
        return None

    _validate_configuration()
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("play", play))
    application.add_handler(CommandHandler("leaderboard", leaderboard))
    application.add_handler(CommandHandler("help", help_command))

    try:
        await application.initialize()
        bot_info = await application.bot.get_me()
        await application.start()
        if application.updater is None:
            raise RuntimeError("Telegram polling updater is unavailable.")
        await application.updater.start_polling(drop_pending_updates=True)
    except Exception:
        if application.updater and application.updater.running:
            await application.updater.stop()
        if application.running:
            await application.stop()
        await application.shutdown()
        raise

    logger.info("Telegram bot @{} connected and polling.", bot_info.username)
    return application


async def stop_bot(application: Application) -> None:
    """Stop polling and release Telegram resources in the correct order."""
    if application.updater and application.updater.running:
        await application.updater.stop()
    if application.running:
        await application.stop()
    await application.shutdown()
    logger.info("Telegram bot stopped.")
