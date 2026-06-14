from fastapi import FastAPI

app = FastAPI(title="Habit Tracker API")


@app.get("/health")
async def check_health() -> dict[str, str]:
    """Check backend service health."""
    return {"status": "ok"}