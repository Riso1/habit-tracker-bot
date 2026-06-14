import os
from typing import Any

import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")


def register_user(
    telegram_id: int,
    username: str | None,
    password: str,
) -> dict[str, Any]:
    """Register user in backend."""
    response = requests.post(
        f"{BACKEND_URL}/auth/register",
        json={
            "telegram_id": telegram_id,
            "username": username,
            "password": password,
        },
        timeout=10,
    )

    if response.status_code == 409:
        return {}

    response.raise_for_status()
    return response.json()


def get_token(telegram_id: int, username: str | None, password: str) -> str:
    """Get JWT token from backend."""
    response = requests.post(
        f"{BACKEND_URL}/auth/token",
        json={
            "telegram_id": telegram_id,
            "username": username,
            "password": password,
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def get_habits(token: str) -> list[dict[str, Any]]:
    """Get user habits."""
    response = requests.get(
        f"{BACKEND_URL}/habits/",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()
