from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.habits import router as habits_router

app = FastAPI(title="Habit Tracker API")

app.include_router(auth_router)
app.include_router(habits_router)


@app.get("/health")
async def check_health() -> dict[str, str]:
    """Check backend service health."""
    return {"status": "ok"}
