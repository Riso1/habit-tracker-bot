from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.models.user import User
from app.services.token import decode_access_token
from app.services.user import get_user_by_telegram_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
) -> User:
    """Get current user by JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        telegram_id = decode_access_token(token)
    except JWTError as error:
        raise credentials_exception from error

    user = await get_user_by_telegram_id(session, telegram_id)

    if user is None:
        raise credentials_exception

    return user
