from typing import List
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, OperationalError

from app.domains.questions.repository import QuestionRepository
from app.domains.questions.schemas import (
    QuestionCreateSchema,
    QuestionResponseSchema,
    QuestionWithAnswersSchema
)


class QuestionService:
    """Сервис для работы с вопросами (бизнес-логика)"""

    def __init__(self, repository: QuestionRepository):
        self.repository = repository

    async def get_all_questions(self) -> List[QuestionResponseSchema]:
        """Получить список всех вопросов"""
        questions = await self.repository.get_all()
        return [QuestionResponseSchema.model_validate(question) for question in questions]

    async def get_question_by_id(self, question_id: int) -> QuestionWithAnswersSchema:
        """Получить вопрос по ID с проверкой существования"""
        question = await self.repository.get_by_id_with_answers(question_id)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question with ID {question_id} not found"
            )
        return QuestionWithAnswersSchema.model_validate(question)

    async def create_question(self, question_data: QuestionCreateSchema) -> QuestionResponseSchema:
        """Создать новый вопрос"""
        try:
            question = await self.repository.create(question_data)
            return QuestionResponseSchema.model_validate(question)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data integrity error when creating question"
            )
        except OperationalError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection error"
            )

    async def delete_question(self, question_id: int) -> None:
        """Удалить вопрос с проверкой существования"""
        # Удаляем вопрос
        deleted = await self.repository.delete(question_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question with ID {question_id} not found"
            )
