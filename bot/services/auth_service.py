from services.api_client import get_token, register_user
from storage.token_storage import save_user_token


def build_user_password(telegram_id: int) -> str:
    """Build service password for Telegram user."""
    return f"telegram-{telegram_id}"


def authenticate_user(telegram_id: int, username: str | None) -> str:
    """Register user if needed, get token and save it."""
    password = build_user_password(telegram_id)

    register_user(telegram_id, username, password)
    token = get_token(telegram_id, username, password)

    save_user_token(
        telegram_id=telegram_id,
        username=username,
        password=password,
        access_token=token,
    )

    return token


def refresh_user_token(
    telegram_id: int,
    username: str | None,
    password: str,
) -> str:
    """Refresh user token and save it."""
    token = get_token(telegram_id, username, password)

    save_user_token(
        telegram_id=telegram_id,
        username=username,
        password=password,
        access_token=token,
    )

    return token