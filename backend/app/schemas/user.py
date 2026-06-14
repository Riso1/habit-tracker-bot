from pydantic import BaseModel, ConfigDict


class UserCreateSchema(BaseModel):
    """Schema for user registration."""

    telegram_id: int
    username: str | None = None
    password: str


class UserReadSchema(BaseModel):
    """Schema for reading user data."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    telegram_id: int
    username: str | None = None