from typing import Any

import requests

from config.settings import BACKEND_URL


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


def create_habit(
    token: str,
    title: str,
    description: str | None = None,
    target_days: int = 21,
) -> dict[str, Any]:
    """Create user habit."""
    response = requests.post(
        f"{BACKEND_URL}/habits/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": title,
            "description": description,
            "target_days": target_days,
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def complete_habit(token: str, habit_id: int) -> dict[str, Any]:
    """Mark habit as completed."""
    response = requests.post(
        f"{BACKEND_URL}/habits/{habit_id}/complete",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def skip_habit(token: str, habit_id: int) -> dict[str, Any]:
    """Mark habit as not completed."""
    response = requests.post(
        f"{BACKEND_URL}/habits/{habit_id}/skip",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def update_habit(token: str, habit_id: int, title: str) -> dict[str, Any]:
    """Update user habit title."""
    response = requests.patch(
        f"{BACKEND_URL}/habits/{habit_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": title},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def delete_habit(token: str, habit_id: int) -> None:
    """Delete user habit."""
    response = requests.delete(
        f"{BACKEND_URL}/habits/{habit_id}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    response.raise_for_status()
