from telebot import TeleBot
from telebot.types import Message

from services.auth_service import authenticate_user


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


def register_common_handlers(bot: TeleBot) -> None:
    """Register common bot handlers."""

    @bot.message_handler(commands=["start"])
    def handle_start(message: Message) -> None:
        """Register user and save access token."""
        telegram_id = message.from_user.id
        username = message.from_user.username

        try:
            authenticate_user(telegram_id, username)
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