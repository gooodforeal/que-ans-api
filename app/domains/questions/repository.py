from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.base_repository import BaseRepository
from app.domains.questions.model import Question
from app.domains.questions.schemas import QuestionCreateSchema
from app.utils.logger import get_logger

logger = get_logger(__name__)


class QuestionRepository(BaseRepository[Question]):
    """Репозиторий для работы с вопросами"""

    def __init__(self, db: AsyncSession):
        super().__init__(db, Question)

    async def get_all(self) -> List[Question]:
        """Получить все вопросы"""
        logger.info("Получение списка всех вопросов")
        result = await self.db.execute(
            select(Question).order_by(Question.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_id_with_answers(self, question_id: int) -> Optional[Question]:
        """Получить вопрос по ID с загрузкой ответов"""
        logger.info(f"Получение вопроса с ID: {question_id} с ответами")
        result = await self.db.execute(
            select(Question)
            .options(selectinload(Question.answers))
            .filter(Question.id == question_id)
        )
        return result.scalar_one_or_none()

    async def create(self, question_data: QuestionCreateSchema) -> Question:
        """Создать новый вопрос"""
        logger.info("Создание нового вопроса")
        try:
            question = Question(text=question_data.text)
            self.db.add(question)
            await self.db.commit()
            await self.db.refresh(question)
            logger.info(f"Вопрос создан с ID: {question.id}")
            return question
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Ошибка при создании вопроса: {str(e)}")
            raise

    async def delete(self, question_id: int) -> bool:
        """Удалить вопрос (каскадно удалятся все ответы)"""
        logger.info(f"Удаление вопроса с ID: {question_id}")
        try:
            # Загружаем вопрос с ответами для каскадного удаления через ORM
            result = await self.db.execute(
                select(Question)
                .options(selectinload(Question.answers))
                .filter(Question.id == question_id)
            )
            question = result.scalar_one_or_none()

            if not question:
                logger.warning(f"Вопрос с ID {question_id} не найден")
                return False

            # Удаляем через ORM для работы каскадного удаления
            await self.db.delete(question)
            await self.db.commit()
            logger.info(f"Вопрос с ID {question_id} удален")
            return True
        except Exception as e:
            await self.db.rollback()
            logger.error(
                f"Ошибка при удалении вопроса с ID {question_id}: {str(e)}"
            )
            raise
