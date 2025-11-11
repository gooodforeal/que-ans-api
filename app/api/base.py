from fastapi import APIRouter

from app.utils.config import settings
from app.core.schemas import StandardResponse

# Базовый роутер для общих endpoints
base_router = APIRouter()


@base_router.get("/", response_model=StandardResponse[dict])
def root():
    """Корневой endpoint"""
    return StandardResponse(
        message="Questions and Answers API",
        data={
            "version": settings.api_version,
            "docs": "/docs"
        }
    )


@base_router.get("/health", response_model=StandardResponse[dict])
def health_check():
    """Проверка здоровья приложения"""
    return StandardResponse(
        message="Service is healthy",
        data={"status": "healthy"}
    )

