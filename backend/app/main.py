from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.api.router import router
from app.core.config import settings
from app.core.logging import logger
from app.core.handlers import register_exception_handlers

logger.info("Starting Legal Intelligence Platform API")
PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIR = PROJECT_ROOT / "frontend"

app =FastAPI(
    title=settings.APP_NAME,
    description="Backend API for the Legal Intelligence Platform",
    version=settings.APP_VERSION,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)
register_exception_handlers(app)
app.include_router(router)

if FRONTEND_DIR.is_dir():
    app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")

    @app.get("/", include_in_schema=False)
    def serve_frontend() -> FileResponse:
        return FileResponse(FRONTEND_DIR / "index.html")
