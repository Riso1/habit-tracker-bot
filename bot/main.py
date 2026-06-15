import telebot

from config.settings import BOT_TOKEN
from handlers.common import register_common_handlers
from handlers.habits import register_habit_handlers
from storage.token_storage import init_token_storage

bot = telebot.TeleBot(
    BOT_TOKEN,
    parse_mode=None,
)

register_common_handlers(bot)
register_habit_handlers(bot)

if __name__ == "__main__":
    init_token_storage()
    bot.infinity_polling()