from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.schemas.habit import HabitCreateSchema, HabitUpdateSchema


async def get_user_habits(session: AsyncSession, user_id: int) -> list[Habit]:
    """Get active user habits."""
    result = await session.execute(
        select(Habit).where(Habit.user_id == user_id, Habit.is_active.is_(True))
    )
    return list(result.scalars().all())


async def get_user_habit(
    session: AsyncSession,
    user_id: int,
    habit_id: int,
) -> Habit | None:
    """Get one user habit."""
    result = await session.execute(
        select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def create_habit(
    session: AsyncSession,
    user_id: int,
    habit_data: HabitCreateSchema,
) -> Habit:
    """Create new habit."""
    habit = Habit(user_id=user_id, **habit_data.model_dump())
    session.add(habit)
    await session.commit()
    await session.refresh(habit)
    return habit


async def update_habit(
    session: AsyncSession,
    habit: Habit,
    habit_data: HabitUpdateSchema,
) -> Habit:
    """Update habit."""
    update_data = habit_data.model_dump(exclude_unset=True)

    for field_name, field_value in update_data.items():
        setattr(habit, field_name, field_value)

    await session.commit()
    await session.refresh(habit)
    return habit


async def delete_habit(session: AsyncSession, habit: Habit) -> None:
    """Delete habit."""
    await session.delete(habit)
    await session.commit()


async def mark_habit_completion(
    session: AsyncSession,
    habit: Habit,
    is_completed: bool,
) -> HabitLog:
    """Mark habit completion for today."""
    today = date.today()

    result = await session.execute(
        select(HabitLog).where(
            HabitLog.habit_id == habit.id,
            HabitLog.log_date == today,
        )
    )
    habit_log = result.scalar_one_or_none()

    if habit_log is None:
        habit_log = HabitLog(
            habit_id=habit.id,
            log_date=today,
            is_completed=is_completed,
        )
        session.add(habit_log)
    else:
        habit_log.is_completed = is_completed

    if is_completed and habit.completed_count < habit.target_days:
        habit.completed_count += 1

    if habit.completed_count >= habit.target_days:
        habit.is_active = False

    await session.commit()
    await session.refresh(habit_log)
    return habit_log