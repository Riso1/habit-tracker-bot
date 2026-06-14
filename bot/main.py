import os

import telebot
from telebot.types import Message

from api_client import (
    complete_habit,
    create_habit,
    get_habits,
    get_token,
    register_user,
    skip_habit,
)

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
        "/habits — список привычек\n"
        "/add_habit — создать привычку\n"
        "/complete_habit — отметить выполнение",
        "/skip_habit — отметить невыполнение",
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


@bot.message_handler(commands=["add_habit"])
def handle_add_habit(message: Message) -> None:
    """Ask user for habit title."""
    telegram_id = message.from_user.id

    if telegram_id not in user_tokens:
        bot.send_message(message.chat.id, "Сначала выполните /start.")
        return

    bot.send_message(message.chat.id, "Введите название новой привычки:")
    bot.register_next_step_handler(message, process_habit_title)


def process_habit_title(message: Message) -> None:
    """Create habit after title input."""
    telegram_id = message.from_user.id
    token = user_tokens.get(telegram_id)

    if token is None:
        bot.send_message(message.chat.id, "Сначала выполните /start.")
        return

    habit_title = message.text.strip()

    if not habit_title:
        bot.send_message(message.chat.id, "Название привычки не может быть пустым.")
        return

    try:
        habit = create_habit(
            token=token,
            title=habit_title,
            description="Создана через Telegram",
            target_days=21,
        )
    except Exception:
        bot.send_message(message.chat.id, "Не удалось создать привычку.")
        return

    bot.send_message(
        message.chat.id,
        f"Привычка создана!\n"
        f"ID: {habit['id']}\n"
        f"Название: {habit['title']}",
    )


@bot.message_handler(commands=["complete_habit"])
def handle_complete_habit(message: Message) -> None:
    """Ask user for completed habit ID."""
    telegram_id = message.from_user.id

    if telegram_id not in user_tokens:
        bot.send_message(message.chat.id, "Сначала выполните /start.")
        return

    bot.send_message(message.chat.id, "Введите ID выполненной привычки:")
    bot.register_next_step_handler(message, process_complete_habit_id)


def process_complete_habit_id(message: Message) -> None:
    """Complete habit after ID input."""
    telegram_id = message.from_user.id
    token = user_tokens.get(telegram_id)

    if token is None:
        bot.send_message(message.chat.id, "Сначала выполните /start.")
        return

    if not message.text.isdigit():
        bot.send_message(message.chat.id, "ID должен быть числом.")
        return

    habit_id = int(message.text)

    try:
        complete_habit(token, habit_id)
    except Exception:
        bot.send_message(message.chat.id, "Не удалось отметить привычку.")
        return

    bot.send_message(
        message.chat.id,
        f"Привычка №{habit_id} отмечена как выполненная.",
    )


@bot.message_handler(commands=["skip_habit"])
def handle_skip_habit(message: Message) -> None:
    """Ask user for skipped habit ID."""
    telegram_id = message.from_user.id

    if telegram_id not in user_tokens:
        bot.send_message(message.chat.id, "Сначала выполните /start.")
        return

    bot.send_message(message.chat.id, "Введите ID невыполненной привычки:")
    bot.register_next_step_handler(message, process_skip_habit_id)


def process_skip_habit_id(message: Message) -> None:
    """Skip habit after ID input."""
    telegram_id = message.from_user.id
    token = user_tokens.get(telegram_id)

    if token is None:
        bot.send_message(message.chat.id, "Сначала выполните /start.")
        return

    if not message.text.isdigit():
        bot.send_message(message.chat.id, "ID должен быть числом.")
        return

    habit_id = int(message.text)

    try:
        skip_habit(token, habit_id)
    except Exception:
        bot.send_message(message.chat.id, "Не удалось отметить привычку.")
        return

    bot.send_message(
        message.chat.id,
        f"Привычка №{habit_id} отмечена как невыполненная.",
    )


if __name__ == "__main__":
    bot.infinity_polling()
