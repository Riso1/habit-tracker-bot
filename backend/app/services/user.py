from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreateSchema
from app.services.password import create_password_hash


async def get_user_by_telegram_id(
    session: AsyncSession,
    telegram_id: int,
) -> User | None:
    """Get user by Telegram ID."""
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    return result.scalar_one_or_none()


async def create_user(
    session: AsyncSession,
    user_data: UserCreateSchema,
) -> User:
    """Create new user."""
    user = User(
        telegram_id=user_data.telegram_id,
        username=user_data.username,
        password_hash=create_password_hash(user_data.password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
