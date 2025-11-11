from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.utils.config import settings
from app.utils.logger import setup_logging
from app.core.database import engine
from app.core.schemas import StandardResponse
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
