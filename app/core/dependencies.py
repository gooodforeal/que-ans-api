from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.questions.repository import QuestionRepository
from app.questions.service import QuestionService
from app.answers.repository import AnswerRepository
from app.answers.service import AnswerService


def get_question_repository(db: AsyncSession = Depends(get_db)) -> QuestionRepository:
    """Dependency для получения репозитория вопросов"""
    return QuestionRepository(db)


def get_answer_repository(db: AsyncSession = Depends(get_db)) -> AnswerRepository:
    """Dependency для получения репозитория ответов"""
    return AnswerRepository(db)


def get_question_service(
    repository: QuestionRepository = Depends(get_question_repository)
) -> QuestionService:
    """Dependency для получения сервиса вопросов"""
    return QuestionService(repository)


def get_answer_service(
    repository: AnswerRepository = Depends(get_answer_repository)
) -> AnswerService:
    """Dependency для получения сервиса ответов"""
    return AnswerService(repository)
