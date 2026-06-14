from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_async_session
from app.models.user import User
from app.schemas.user import UserCreateSchema, UserReadSchema
from app.services.password import verify_password
from app.services.token import create_access_token
from app.services.user import create_user, get_user_by_telegram_id

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserReadSchema)
async def register_user(
    user_data: UserCreateSchema,
    session: AsyncSession = Depends(get_async_session),
) -> User:
    """Register new user."""
    existing_user = await get_user_by_telegram_id(session, user_data.telegram_id)

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )

    return await create_user(session, user_data)


@router.post("/token")
async def create_user_token(
    user_data: UserCreateSchema,
    session: AsyncSession = Depends(get_async_session),
) -> dict[str, str]:
    """Create access token for user."""
    user = await get_user_by_telegram_id(session, user_data.telegram_id)

    if user is None or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Telegram ID or password",
        )

    access_token = create_access_token(user.telegram_id)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserReadSchema)
async def read_current_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Read current authenticated user."""
    return current_user
