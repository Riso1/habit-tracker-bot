import os
import time

import schedule
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is not set")

bot = telebot.TeleBot(BOT_TOKEN)


def send_daily_reminders() -> None:
    """Placeholder for daily habit reminders."""
    print("Daily reminder check started", flush=True)


schedule.every().day.at("09:00").do(send_daily_reminders)

if __name__ == "__main__":
    send_daily_reminders()

    while True:
        schedule.run_pending()
        time.sleep(60)
        