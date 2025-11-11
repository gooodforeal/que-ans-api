from contextlib import asynccontextmanager

from app.core.database import engine


@asynccontextmanager
async def lifespan(app):
    """Управление жизненным циклом приложения"""
    # Startup
    yield
    # Shutdown
    await engine.dispose()
