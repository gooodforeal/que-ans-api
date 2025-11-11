from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.answers.schemas import AnswerResponseSchema


class QuestionBaseSchema(BaseModel):
    text: str = Field(..., min_length=1, max_length=200, description="Текст вопроса")


class QuestionCreateSchema(QuestionBaseSchema):
    pass


class QuestionResponseSchema(QuestionBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class QuestionWithAnswersSchema(QuestionResponseSchema):
    answers: List["AnswerResponseSchema"] = []


# Импортируем для правильной работы forward references
from app.answers.schemas import AnswerResponseSchema  # noqa
QuestionWithAnswersSchema.model_rebuild()
