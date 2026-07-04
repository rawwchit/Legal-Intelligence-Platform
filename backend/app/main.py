from fastapi import FastAPI
from app.api.router import router
from app.core.config import settings
from app.core.logging import logger

logger.info("Starting Legal Intelligence Platform API")
app =FastAPI(
    title=settings.APP_NAME,
    description="Backend API for the Legal Intelligence Platform",
    version=settings.APP_VERSION,
)
app.include_router(router)