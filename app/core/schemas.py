from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar('T')


class StandardResponse(BaseModel, Generic[T]):
    """Стандартный формат ответа API"""
    message: str
    data: Optional[T] = None

    class Config:
        from_attributes = True
