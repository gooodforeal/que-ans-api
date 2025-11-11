from pydantic import BaseModel, Field
from datetime import datetime


class AnswerBaseSchema(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="Текст ответа")
    user_id: int = Field(..., gt=0, description="Идентификатор пользователя")


class AnswerCreateSchema(AnswerBaseSchema):
    pass


class AnswerResponseSchema(AnswerBaseSchema):
    id: int
    question_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
