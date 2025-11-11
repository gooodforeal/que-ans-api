from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, OperationalError

from app.answers.repository import AnswerRepository
from app.answers.schemas import AnswerCreateSchema, AnswerResponseSchema


class AnswerService:
    """Сервис для работы с ответами (бизнес-логика)"""

    def __init__(self, repository: AnswerRepository):
        self.repository = repository

    async def create_answer(
        self,
        question_id: int,
        answer_data: AnswerCreateSchema
    ) -> AnswerResponseSchema:
        """Создать ответ к вопросу с обработкой ошибок"""
        try:
            answer = await self.repository.create(question_id, answer_data)
            return AnswerResponseSchema.model_validate(answer)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data integrity error when creating answer"
            )
        except OperationalError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection error"
            )

    async def get_answer_by_id(self, answer_id: int) -> AnswerResponseSchema:
        """Получить ответ по ID с проверкой существования"""
        answer = await self.repository.get_by_id(answer_id)
        if not answer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Answer with ID {answer_id} not found"
            )
        return AnswerResponseSchema.model_validate(answer)

    async def delete_answer(self, answer_id: int) -> None:
        """Удалить ответ с проверкой существования"""
        deleted = await self.repository.delete(answer_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Answer with ID {answer_id} not found"
            )
