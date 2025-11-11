from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_answer_service
from app.core.schemas import StandardResponse
from app.domains.answers.schemas import AnswerCreateSchema, AnswerResponseSchema
from app.domains.answers.service import AnswerService

# Роутер для создания ответов (с префиксом /questions)
answer_create_router = APIRouter(prefix="/questions", tags=["answers"])

# Роутер для получения и удаления ответов (без префикса)
answers_router = APIRouter(prefix="/answers", tags=["answers"])


@answer_create_router.post(
    "/{question_id}/answers/",
    response_model=StandardResponse[AnswerResponseSchema],
    status_code=status.HTTP_201_CREATED
)
async def create_answer(
    question_id: int,
    answer_data: AnswerCreateSchema,
    answer_service: AnswerService = Depends(get_answer_service)
):
    """Добавить ответ к вопросу"""
    answer = await answer_service.create_answer(question_id, answer_data)
    return StandardResponse(
        message="Answer created successfully",
        data=answer
    )


@answers_router.get(
    "/{answer_id}",
    response_model=StandardResponse[AnswerResponseSchema],
    status_code=status.HTTP_200_OK
)
async def get_answer(
    answer_id: int,
    answer_service: AnswerService = Depends(get_answer_service)
):
    """Получить конкретный ответ"""
    answer = await answer_service.get_answer_by_id(answer_id)
    return StandardResponse(
        message="Answer retrieved successfully",
        data=answer
    )


@answers_router.delete(
    "/{answer_id}",
    response_model=StandardResponse[dict],
    status_code=status.HTTP_200_OK
)
async def delete_answer(
    answer_id: int,
    answer_service: AnswerService = Depends(get_answer_service)
):
    """Удалить ответ"""
    await answer_service.delete_answer(answer_id)
    return StandardResponse(
        message="Answer deleted successfully",
        data={"id": answer_id}
    )
