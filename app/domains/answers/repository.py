from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.base_repository import BaseRepository
from app.domains.answers.model import Answer
from app.domains.questions.model import Question
from app.domains.answers.schemas import AnswerCreateSchema
from app.utils.logger import get_logger

logger = get_logger(__name__)


class AnswerRepository(BaseRepository[Answer]):
    """Репозиторий для работы с ответами"""

    def __init__(self, db: AsyncSession):
        super().__init__(db, Answer)

    async def create(self, question_id: int, answer_data: AnswerCreateSchema) -> Answer:
        """Создать новый ответ к вопросу"""
        logger.info(f"Создание ответа для вопроса с ID: {question_id}")

        try:
            # Проверка существования вопроса
            result = await self.db.execute(
                select(Question).filter(Question.id == question_id)
            )
            question = result.scalar_one_or_none()
            if not question:
                logger.error(f"Question with ID {question_id} not found")
                raise ValueError(f"Question with ID {question_id} does not exist")

            answer = Answer(
                question_id=question_id,
                text=answer_data.text,
                user_id=answer_data.user_id
            )
            self.db.add(answer)
            await self.db.commit()
            await self.db.refresh(answer)
            logger.info(f"Ответ создан с ID: {answer.id}")
            return answer
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error creating answer: {str(e)}")
            raise

    async def delete(self, answer_id: int) -> bool:
        """Удалить ответ"""
        return await super().delete(answer_id)
