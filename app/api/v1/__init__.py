from fastapi import APIRouter

from app.api.v1 import questions, answers

# Главный роутер для v1 API
api_router = APIRouter(prefix="/api/v1")

# Подключаем роутеры
api_router.include_router(questions.router)
api_router.include_router(answers.answer_create_router)
api_router.include_router(answers.answers_router)

