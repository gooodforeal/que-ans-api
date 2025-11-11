from typing import Optional, TypeVar, Generic, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import DeclarativeBase

from app.utils.logger import get_logger

logger = get_logger(__name__)

# Тип для модели
ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class BaseRepository(Generic[ModelType]):
    """Базовый репозиторий с общими методами для работы с БД"""

    def __init__(self, db: AsyncSession, model: Type[ModelType]):
        """
        Инициализация репозитория

        Args:
            db: Асинхронная сессия БД
            model: Класс модели SQLAlchemy
        """
        self.db = db
        self.model = model

    async def get_by_id(self, entity_id: int) -> Optional[ModelType]:
        """
        Получить сущность по ID

        Args:
            entity_id: ID сущности

        Returns:
            Сущность или None, если не найдена
        """
        logger.info(f"Получение {self.model.__name__} с ID: {entity_id}")
        result = await self.db.execute(
            select(self.model).filter(self.model.id == entity_id)
        )
        return result.scalar_one_or_none()

    async def delete(self, entity_id: int) -> bool:
        """
        Удалить сущность по ID

        Args:
            entity_id: ID сущности

        Returns:
            True если удалено, False если не найдено
        """
        logger.info(f"Удаление {self.model.__name__} с ID: {entity_id}")
        try:
            # Удаляем через statement для надежности с async сессиями
            result = await self.db.execute(
                delete(self.model).where(self.model.id == entity_id)
            )
            await self.db.commit()
            if result.rowcount > 0:
                logger.info(f"{self.model.__name__} с ID {entity_id} удален")
                return True
            else:
                logger.warning(f"{self.model.__name__} с ID {entity_id} не найден")
                return False
        except Exception as e:
            await self.db.rollback()
            logger.error(
                f"Ошибка при удалении {self.model.__name__} "
                f"с ID {entity_id}: {str(e)}"
            )
            raise
