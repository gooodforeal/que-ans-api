from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager

from app.utils.config import settings
from app.utils.logger import setup_logging
from app.core.database import engine
from app.core.schemas import StandardResponse
from app.core.exceptions import http_exception_handler, validation_exception_handler
from app.api.v1 import api_router

# Настройка логирования
setup_logging()


@asynccontextmanager
async def lifespan(app):
    """Управление жизненным циклом приложения"""
    # Startup
    yield
    # Shutdown
    await engine.dispose()


# Создание приложения
app = FastAPI(
    title=settings.project_name,
    version=settings.api_version,
    description="API-сервис для вопросов и ответов",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение обработчиков исключений
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Подключение роутеров API v1
app.include_router(api_router)


@app.get("/", response_model=StandardResponse[dict])
def root():
    """Корневой endpoint"""
    return StandardResponse(
        message="Questions and Answers API",
        data={
            "version": settings.api_version,
            "docs": "/docs"
        }
    )


@app.get("/health", response_model=StandardResponse[dict])
def health_check():
    """Проверка здоровья приложения"""
    return StandardResponse(
        message="Service is healthy",
        data={"status": "healthy"}
    )
