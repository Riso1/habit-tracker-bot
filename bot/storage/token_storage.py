import sqlite3

from config.settings import TOKEN_DB_PATH


def init_token_storage() -> None:
    """Create token storage table if it does not exist."""
    with sqlite3.connect(TOKEN_DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS user_tokens (
                telegram_id INTEGER PRIMARY KEY,
                username TEXT,
                password TEXT NOT NULL,
                access_token TEXT NOT NULL
            )
            """
        )


def save_user_token(
    telegram_id: int,
    username: str | None,
    password: str,
    access_token: str,
) -> None:
    """Save or update user token."""
    with sqlite3.connect(TOKEN_DB_PATH) as connection:
        connection.execute(
            """
            INSERT INTO user_tokens (
                telegram_id,
                username,
                password,
                access_token
            )
            VALUES (?, ?, ?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET
                username = excluded.username,
                password = excluded.password,
                access_token = excluded.access_token
            """,
            (telegram_id, username, password, access_token),
        )


def get_user_token(telegram_id: int) -> str | None:
    """Get saved user access token."""
    with sqlite3.connect(TOKEN_DB_PATH) as connection:
        cursor = connection.execute(
            """
            SELECT access_token
            FROM user_tokens
            WHERE telegram_id = ?
            """,
            (telegram_id,),
        )
        row = cursor.fetchone()

    if row is None:
        return None

    return str(row[0])


def get_user_credentials(telegram_id: int) -> tuple[str | None, str] | None:
    """Get saved user credentials for token refresh."""
    with sqlite3.connect(TOKEN_DB_PATH) as connection:
        cursor = connection.execute(
            """
            SELECT username, password
            FROM user_tokens
            WHERE telegram_id = ?
            """,
            (telegram_id,),
        )
        row = cursor.fetchone()

    if row is None:
        return None

    username, password = row
    return username, password