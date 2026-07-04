from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.exceptions import (
    AppException,
    ResourceNotFoundException,
    AuthenticationException,
    AIServiceException,
)
from app.core.logging import logger

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(ResourceNotFoundException)
    async def resource_not_found_handler(
        request: Request,
        exc: ResourceNotFoundException,
    ):
        logger.warning(exc.message)

        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": exc.message,
            },
        )

    @app.exception_handler(AuthenticationException)
    async def authentication_handler(
        request: Request,
        exc: AuthenticationException,
    ):
        logger.warning(exc.message)

        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": exc.message,
            },
        )

    @app.exception_handler(AIServiceException)
    async def ai_service_handler(
        request: Request,
        exc: AIServiceException,
    ):
        logger.error(exc.message)

        return JSONResponse(
            status_code=503,
            content={
                "success": False,
                "message": exc.message,
            },
        )

    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request,
        exc: AppException,
    ):
        logger.error(exc.message)

        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": exc.message,
            },
        )