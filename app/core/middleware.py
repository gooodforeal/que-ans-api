from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.utils.config import settings


def setup_middleware(app: FastAPI) -> None:
    """Настройка middleware для приложения"""
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
