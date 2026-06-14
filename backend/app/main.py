from fastapi import FastAPI

from app.api.auth import router as auth_router

app = FastAPI(title="Habit Tracker API")

app.include_router(auth_router)


@app.get("/health")
async def check_health() -> dict[str, str]:
    """Check backend service health."""
    return {"status": "ok"}