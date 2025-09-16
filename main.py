from fastapi import FastAPI
from app.routers import pushups, squats

app = FastAPI(title="Fitness AI Analysis")

# Include routers
app.include_router(pushups.router, prefix="/pushups", tags=["Pushups"])
app.include_router(squats.router, prefix="/squats", tags=["Squats"])
