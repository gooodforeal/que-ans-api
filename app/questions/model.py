from sqlalchemy import Column, Text, Index
from sqlalchemy.orm import relationship

from app.core.base_model import BaseModel


class Question(BaseModel):
    __tablename__ = "questions"
    __table_args__ = (
        Index('ix_questions_id', 'id'),
    )

    text = Column(Text, nullable=False)

    answers = relationship(
        "Answer",
        back_populates="question",
        cascade="all, delete-orphan"
    )
