import os

import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is not set")

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def handle_start(message: telebot.types.Message) -> None:
    """Handle start command."""
    bot.send_message(
        message.chat.id,
        "Привет! Я бот для трекинга привычек.\n"
        "Скоро здесь появятся команды для работы с привычками.",
    )


if __name__ == "__main__":
    bot.infinity_polling()
