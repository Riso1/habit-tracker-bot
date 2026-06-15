import requests

from services.api_client import get_habits
from services.auth_service import refresh_user_token
from storage.token_storage import (
    get_user_credentials,
    get_user_token,
)


def get_user_habits(telegram_id: int) -> list[dict]:
    """Get habits with automatic token refresh."""
    token = get_user_token(telegram_id)

    if token is None:
        return []

    try:
        return get_habits(token)

    except requests.HTTPError as error:
        status_code = error.response.status_code

        if status_code != 401:
            raise

    credentials = get_user_credentials(telegram_id)

    if credentials is None:
        return []

    username, password = credentials

    new_token = refresh_user_token(
        telegram_id,
        username,
        password,
    )

    return get_habits(new_token)