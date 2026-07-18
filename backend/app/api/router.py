from fastapi import APIRouter

from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.documents import router as document_router

router = APIRouter()

router.include_router(health_router, prefix="/api/v1")
router.include_router(auth_router, prefix="/api/v1/auth")
router.include_router(
    document_router,
    prefix="/api/v1/documents",
    tags=["Documents"],
)