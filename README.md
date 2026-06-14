# Habit Tracker Bot

Telegram-бот для трекинга привычек с backend-сервисом на FastAPI.

## Стек

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- PyTelegramBotAPI
- Docker Compose
- Poetry
- JWT

## Запуск

1. Создать файл `.env` на основе `.env.template`.

2. Указать токен Telegram-бота:

```env
BOT_TOKEN=your_telegram_bot_token
JWT_SECRET_KEY=your_random_secret_key
```

`JWT_SECRET_KEY` должен быть случайной длинной строкой. Его можно сгенерировать командой:

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
````

3. Запустить проект:

```bash
docker compose up --build
```

4. Применить миграции:

```bash
docker exec -it habits_backend alembic upgrade head
```

## Backend

Документация API:

```text
http://127.0.0.1:8000/docs
```

Проверка сервиса:

```text
http://127.0.0.1:8000/health
```

## Команды бота

- `/start` — регистрация и авторизация пользователя
- `/habits` — список привычек
- `/add_habit` — добавить привычку
- `/complete_habit` — отметить выполнение привычки
- `/skip_habit` — отметить невыполнение привычки
- `/edit_habit` — изменить привычку
- `/delete_habit` — удалить привычку
