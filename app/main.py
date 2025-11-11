from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.utils.config import settings
from app.utils.logger import setup_logging
from app.core.exceptions import http_exception_handler, validation_exception_handler
from app.core.lifespan import lifespan
from app.core.middleware import setup_middleware
from app.api.base import base_router
from app.api.v1 import api_router

# Настройка логирования
setup_logging()


# Создание приложения
app = FastAPI(
    title=settings.project_name,
    version=settings.api_version,
    description="API-сервис для вопросов и ответов",
    lifespan=lifespan
)

# Настройка middleware
setup_middleware(app)

# Подключение обработчиков исключений
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Подключение базового роутера
app.include_router(base_router)

# Подключение роутеров API v1
app.include_router(api_router)
