import os

import telebot
from telebot.types import Message

from storage.token_storage import get_user_token, init_token_storage

from services.auth_service import authenticate_user

from services.api_client import (
    complete_habit,
    create_habit,
    delete_habit,
    get_habits,
    skip_habit,
    update_habit,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is not set")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)


def get_help_text() -> str:
    """Return bot help text."""
    return (
        "Доступные команды:\n"
        "/start — запуск бота\n"
        "/help — список команд\n"
        "/habits — список привычек\n"
        "/add_habit — создать привычку\n"
        "/complete_habit — отметить выполнение\n"
        "/skip_habit — отметить невыполнение\n"
        "/edit_habit — изменить привычку\n"
        "/delete_habit — удалить привычку"
    )


@bot.message_handler(commands=["start"])
def handle_start(message: Message) -> None:
    """Register user and save access token."""
    telegram_id = message.from_user.id
    username = message.from_user.username

    try:
        authenticate_user(
            telegram_id,
            username,
        )
    except Exception:
        bot.send_message(
            message.chat.id,
            "Не удалось подключиться к сервису. Попробуйте позже.",
        )
        return

    bot.send_message(
        message.chat.id,
        "Привет! Я бот для трекинга привычек.\n\n" + get_help_text(),
    )


@bot.message_handler(commands=["help"])
def handle_help(message: Message) -> None:
    """Show available bot commands."""
    bot.send_message(message.chat.id, get_help_text())


@bot.message_handler(commands=["habits"])
def handle_habits(message: Message) -> None:
    """Show current user habits."""
    telegram_id = message.from_user.id
    token = get_user_token(telegram_id)

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

    if get_user_token(telegram_id) is None:
        bot.send_message(message.chat.id, "Сначала выполните /start.")
        return

    bot.send_message(message.chat.id, "Введите название новой привычки:")
    bot.register_next_step_handler(message, process_habit_title)


def process_habit_title(message: Message) -> None:
    """Create habit after title input."""
    telegram_id = message.from_user.id
    token = get_user_token(telegram_id)
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

    if get_user_token(telegram_id) is None:
        bot.send_message(message.chat.id, "Сначала выполните /start.")
        return

    bot.send_message(message.chat.id, "Введите ID выполненной привычки:")
    bot.register_next_step_handler(message, process_complete_habit_id)


def process_complete_habit_id(message: Message) -> None:
    """Complete habit after ID input."""
    telegram_id = message.from_user.id
    token = get_user_token(telegram_id)
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

    if get_user_token(telegram_id) is None:
        bot.send_message(message.chat.id, "Сначала выполните /start.")
        return

    bot.send_message(message.chat.id, "Введите ID невыполненной привычки:")
    bot.register_next_step_handler(message, process_skip_habit_id)


def process_skip_habit_id(message: Message) -> None:
    """Skip habit after ID input."""
    telegram_id = message.from_user.id
    token = get_user_token(telegram_id)
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


@bot.message_handler(commands=["delete_habit"])
def handle_delete_habit(message: Message) -> None:
    """Ask user for deleted habit ID."""
    telegram_id = message.from_user.id

    if get_user_token(telegram_id) is None:
        bot.send_message(message.chat.id, "Сначала выполните /start.")
        return

    bot.send_message(message.chat.id, "Введите ID привычки для удаления:")
    bot.register_next_step_handler(message, process_delete_habit_id)


def process_delete_habit_id(message: Message) -> None:
    """Delete habit after ID input."""
    telegram_id = message.from_user.id
    token = get_user_token(telegram_id)
    if token is None:
        bot.send_message(message.chat.id, "Сначала выполните /start.")
        return

    if not message.text.isdigit():
        bot.send_message(message.chat.id, "ID должен быть числом.")
        return

    habit_id = int(message.text)

    try:
        delete_habit(token, habit_id)
    except Exception:
        bot.send_message(message.chat.id, "Не удалось удалить привычку.")
        return

    bot.send_message(message.chat.id, f"Привычка №{habit_id} удалена.")


@bot.message_handler(commands=["edit_habit"])
def handle_edit_habit(message: Message) -> None:
    """Ask user for habit edit data."""
    telegram_id = message.from_user.id

    if get_user_token(telegram_id) is None:
        bot.send_message(message.chat.id, "Сначала выполните /start.")
        return

    bot.send_message(
        message.chat.id,
        "Введите ID и новое название через точку с запятой.\n"
        "Пример: 3; Читать книгу",
    )
    bot.register_next_step_handler(message, process_edit_habit_data)


def process_edit_habit_data(message: Message) -> None:
    """Edit habit after user input."""
    telegram_id = message.from_user.id
    token = get_user_token(telegram_id)
    if token is None:
        bot.send_message(message.chat.id, "Сначала выполните /start.")
        return

    if ";" not in message.text:
        bot.send_message(message.chat.id, "Нужно ввести в формате: ID; новое название")
        return

    habit_id_text, habit_title = message.text.split(";", maxsplit=1)

    if not habit_id_text.strip().isdigit():
        bot.send_message(message.chat.id, "ID должен быть числом.")
        return

    habit_id = int(habit_id_text.strip())
    habit_title = habit_title.strip()

    if not habit_title:
        bot.send_message(message.chat.id, "Название не может быть пустым.")
        return

    try:
        habit = update_habit(token, habit_id, habit_title)
    except Exception:
        bot.send_message(message.chat.id, "Не удалось изменить привычку.")
        return

    bot.send_message(
        message.chat.id,
        f"Привычка №{habit['id']} обновлена.\n"
        f"Новое название: {habit['title']}",
    )


if __name__ == "__main__":
    init_token_storage()
    bot.infinity_polling()
