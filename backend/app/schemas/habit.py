from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict


class HabitCreateSchema(BaseModel):
    """Schema for habit creation."""

    title: str
    description: str | None = None
    target_days: int = 21
    reminder_time: time | None = None


class HabitUpdateSchema(BaseModel):
    """Schema for habit update."""

    title: str | None = None
    description: str | None = None
    target_days: int | None = None
    reminder_time: time | None = None
    is_active: bool | None = None


class HabitReadSchema(BaseModel):
    """Schema for reading habit data."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None = None
    target_days: int
    completed_count: int
    reminder_time: time | None = None
    is_active: bool
    created_at: datetime


class HabitLogReadSchema(BaseModel):
    """Schema for reading habit log data."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    habit_id: int
    log_date: date
    is_completed: bool
    created_at: datetime