from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_async_session
from app.models.user import User
from app.schemas.habit import HabitCreateSchema, HabitLogReadSchema
from app.schemas.habit import HabitReadSchema, HabitUpdateSchema
from app.services.habit import create_habit, delete_habit, get_user_habit
from app.services.habit import get_user_habits, mark_habit_completion
from app.services.habit import update_habit

router = APIRouter(prefix="/habits", tags=["Habits"])


@router.get("/", response_model=list[HabitReadSchema])
async def read_habits(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Read current user habits."""
    return await get_user_habits(session, current_user.id)


@router.post("/", response_model=HabitReadSchema, status_code=status.HTTP_201_CREATED)
async def add_habit(
    habit_data: HabitCreateSchema,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Create habit for current user."""
    return await create_habit(session, current_user.id, habit_data)


@router.get("/{habit_id}", response_model=HabitReadSchema)
async def read_habit(
    habit_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Read one current user habit."""
    habit = await get_user_habit(session, current_user.id, habit_id)

    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    return habit


@router.patch("/{habit_id}", response_model=HabitReadSchema)
async def edit_habit(
    habit_id: int,
    habit_data: HabitUpdateSchema,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Update current user habit."""
    habit = await get_user_habit(session, current_user.id, habit_id)

    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    return await update_habit(session, habit, habit_data)


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_habit(
    habit_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Delete current user habit."""
    habit = await get_user_habit(session, current_user.id, habit_id)

    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    await delete_habit(session, habit)


@router.post("/{habit_id}/complete", response_model=HabitLogReadSchema)
async def complete_habit(
    habit_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Mark current user habit as completed."""
    habit = await get_user_habit(session, current_user.id, habit_id)

    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    return await mark_habit_completion(session, habit, is_completed=True)


@router.post("/{habit_id}/skip", response_model=HabitLogReadSchema)
async def skip_habit(
    habit_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Mark current user habit as not completed."""
    habit = await get_user_habit(session, current_user.id, habit_id)

    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    return await mark_habit_completion(session, habit, is_completed=False)
