from fastapi import FastAPI
from app.api.router import router
from app.core.config import settings
app =FastAPI(
    title=settings.APP_NAME,
    description="Backend API for the Legal Intelligence Platform",
    version=settings.APP_VERSION,
)
app.include_router(router)