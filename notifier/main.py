import os
import time
from datetime import datetime

import psycopg2
import schedule
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is not set")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)


def get_database_connection():
    """Create PostgreSQL connection."""
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )


def send_habit_reminders() -> None:
    """Send reminders for active habits with configured reminder time."""
    current_time = datetime.now().strftime("%H:%M")

    query = """
        SELECT users.telegram_id, habits.title
        FROM habits
        JOIN users ON users.id = habits.user_id
        WHERE habits.is_active = true
          AND habits.reminder_time IS NOT NULL
          AND to_char(habits.reminder_time, 'HH24:MI') = %s
    """

    try:
        with get_database_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (current_time,))
                reminders = cursor.fetchall()

    except Exception as error:
        print(f"Reminder check failed: {error}", flush=True)
        return

    if not reminders:
        print(f"No reminders for {current_time}", flush=True)
        return

    for telegram_id, habit_title in reminders:
        try:
            bot.send_message(
                telegram_id,
                f"Напоминание: пора выполнить привычку «{habit_title}».",
            )
            print(
                f"Reminder sent to {telegram_id}: {habit_title}",
                flush=True,
            )
        except Exception as error:
            print(
                f"Failed to send reminder to {telegram_id}: {error}",
                flush=True,
            )


schedule.every(1).minutes.do(send_habit_reminders)

if __name__ == "__main__":
    send_habit_reminders()

    while True:
        schedule.run_pending()
        time.sleep(1)
