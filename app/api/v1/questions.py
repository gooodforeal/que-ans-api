from typing import List
from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_question_service
from app.core.schemas import StandardResponse
from app.questions.schemas import (
    QuestionCreateSchema,
    QuestionResponseSchema,
    QuestionWithAnswersSchema
)
from app.questions.service import QuestionService

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get(
    "/",
    response_model=StandardResponse[List[QuestionResponseSchema]],
    status_code=status.HTTP_200_OK
)
async def get_questions(
    question_service: QuestionService = Depends(get_question_service)
):
    """Получить список всех вопросов"""
    questions = await question_service.get_all_questions()
    return StandardResponse(
        message="Questions retrieved successfully",
        data=questions
    )


@router.post(
    "/",
    response_model=StandardResponse[QuestionResponseSchema],
    status_code=status.HTTP_201_CREATED
)
async def create_question(
    question_data: QuestionCreateSchema,
    question_service: QuestionService = Depends(get_question_service)
):
    """Создать новый вопрос"""
    question = await question_service.create_question(question_data)
    return StandardResponse(
        message="Question created successfully",
        data=question
    )


@router.get(
    "/{question_id}",
    response_model=StandardResponse[QuestionWithAnswersSchema],
    status_code=status.HTTP_200_OK
)
async def get_question(
    question_id: int,
    question_service: QuestionService = Depends(get_question_service)
):
    """Получить вопрос и все ответы на него"""
    question = await question_service.get_question_by_id(question_id)
    return StandardResponse(
        message="Question retrieved successfully",
        data=question
    )


@router.delete(
    "/{question_id}",
    response_model=StandardResponse[dict],
    status_code=status.HTTP_200_OK
)
async def delete_question(
    question_id: int,
    question_service: QuestionService = Depends(get_question_service)
):
    """Удалить вопрос (вместе с ответами)"""
    await question_service.delete_question(question_id)
    return StandardResponse(
        message="Question deleted successfully",
        data={"id": question_id}
    )

