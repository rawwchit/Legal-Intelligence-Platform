from fastapi import FastAPI
from app.api.router import router
from app.core.config import settings
from app.core.logging import logger
from app.core.handlers import register_exception_handlers

logger.info("Starting Legal Intelligence Platform API")
app =FastAPI(
    title=settings.APP_NAME,
    description="Backend API for the Legal Intelligence Platform",
    version=settings.APP_VERSION,
)
register_exception_handlers(app)
app.include_router(router)