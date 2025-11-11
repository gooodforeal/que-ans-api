from sqlalchemy import Column, Integer, ForeignKey, Text, Index
from sqlalchemy.orm import relationship

from app.core.base_model import BaseModel


class Answer(BaseModel):
    __tablename__ = "answers"
    __table_args__ = (
        Index('ix_answers_id', 'id'),
    )

    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)

    question = relationship("Question", back_populates="answers")
