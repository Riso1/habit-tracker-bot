import os

import telebot
from telebot.types import Message

from api_client import get_habits, get_token, register_user

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is not set")

bot = telebot.TeleBot(BOT_TOKEN)

user_tokens: dict[int, str] = {}


def build_user_password(telegram_id: int) -> str:
    """Build simple service password for Telegram user."""
    return f"telegram-{telegram_id}"


@bot.message_handler(commands=["start"])
def handle_start(message: Message) -> None:
    """Register user and save access token."""
    telegram_id = message.from_user.id
    username = message.from_user.username
    password = build_user_password(telegram_id)

    try:
        register_user(telegram_id, username, password)
        token = get_token(telegram_id, username, password)
    except Exception:
        bot.send_message(
            message.chat.id,
            "Не удалось подключиться к сервису. Попробуйте позже.",
        )
        return

    user_tokens[telegram_id] = token

    bot.send_message(
        message.chat.id,
        "Привет! Я бот для трекинга привычек.\n\n"
        "Доступные команды:\n"
        "/habits — список привычек",
    )


@bot.message_handler(commands=["habits"])
def handle_habits(message: Message) -> None:
    """Show current user habits."""
    telegram_id = message.from_user.id
    token = user_tokens.get(telegram_id)

    if token is None:
        bot.send_message(message.chat.id, "Сначала выполните команду /start.")
        return

    try:
        habits = get_habits(token)
    except Exception:
        bot.send_message(message.chat.id, "Не удалось получить список привычек.")
        return

    if not habits:
        bot.send_message(message.chat.id, "У вас пока нет привычек.")
        return

    habit_lines = [
        f"{habit['id']}. {habit['title']} — выполнено "
        f"{habit['completed_count']}/{habit['target_days']}"
        for habit in habits
    ]

    bot.send_message(message.chat.id, "\n".join(habit_lines))


if __name__ == "__main__":
    bot.infinity_polling()
    