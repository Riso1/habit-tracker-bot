from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: int

    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int

    @property
    def database_url(self) -> str:
        """Build async database connection URL."""
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()
