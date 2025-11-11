import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_create_question_success(client):
    """Тест успешного создания вопроса"""
    question_text = "Какой язык программирования лучше?"
    response = await client.post(
        "/api/v1/questions/",
        json={"text": question_text}
    )

    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()

    # Проверяем структуру StandardResponse
    assert "message" in response_data
    assert "data" in response_data
    assert response_data["message"] == "Question created successfully"

    # Проверяем данные вопроса
    question = response_data["data"]
    assert question["text"] == question_text
    assert "id" in question
    assert question["id"] > 0
    assert "created_at" in question
    assert "updated_at" in question


@pytest.mark.asyncio
async def test_create_question_empty_text(client):
    """Тест создания вопроса с пустым текстом - должна быть ошибка валидации"""
    response = await client.post(
        "/api/v1/questions/",
        json={"text": ""}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_data = response.json()
    assert "message" in response_data
    assert "data" in response_data
    assert "Validation error" in response_data["message"]


@pytest.mark.asyncio
async def test_create_question_missing_text(client):
    """Тест создания вопроса без текста - должна быть ошибка валидации"""
    response = await client.post(
        "/api/v1/questions/",
        json={}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_data = response.json()
    assert "message" in response_data
    assert "data" in response_data
    assert "Validation error" in response_data["message"]


@pytest.mark.asyncio
async def test_create_question_text_too_long(client):
    """Тест создания вопроса с текстом превышающим максимальную длину"""
    long_text = "a" * 201  # Максимальная длина 200 символов
    response = await client.post(
        "/api/v1/questions/",
        json={"text": long_text}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_data = response.json()
    assert "message" in response_data
    assert "data" in response_data
    assert "Validation error" in response_data["message"]


@pytest.mark.asyncio
async def test_get_all_questions_empty(client):
    """Тест получения пустого списка вопросов"""
    response = await client.get("/api/v1/questions/")

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert "message" in response_data
    assert "data" in response_data
    assert response_data["message"] == "Questions retrieved successfully"
    assert response_data["data"] == []


@pytest.mark.asyncio
async def test_get_all_questions_with_data(client):
    """Тест получения списка всех вопросов"""
    # Создаем несколько вопросов
    question1_text = "Вопрос 1"
    question2_text = "Вопрос 2"

    await client.post("/api/v1/questions/", json={"text": question1_text})
    await client.post("/api/v1/questions/", json={"text": question2_text})

    response = await client.get("/api/v1/questions/")

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert "message" in response_data
    assert "data" in response_data
    assert response_data["message"] == "Questions retrieved successfully"

    questions = response_data["data"]
    assert len(questions) == 2
    assert all("id" in q for q in questions)
    assert all("text" in q for q in questions)
    assert all("created_at" in q for q in questions)
    assert all("updated_at" in q for q in questions)

    # Проверяем, что вопросы содержат ожидаемые тексты
    texts = [q["text"] for q in questions]
    assert question1_text in texts
    assert question2_text in texts


@pytest.mark.asyncio
async def test_get_question_by_id_success(client):
    """Тест успешного получения вопроса по ID"""
    question_text = "Тестовый вопрос"

    # Создаем вопрос
    create_response = await client.post(
        "/api/v1/questions/",
        json={"text": question_text}
    )
    create_data = create_response.json()
    question_id = create_data["data"]["id"]

    # Получаем вопрос
    response = await client.get(f"/api/v1/questions/{question_id}")

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert "message" in response_data
    assert "data" in response_data
    assert response_data["message"] == "Question retrieved successfully"

    question = response_data["data"]
    assert question["id"] == question_id
    assert question["text"] == question_text
    assert "answers" in question
    assert isinstance(question["answers"], list)
    assert "created_at" in question
    assert "updated_at" in question


@pytest.mark.asyncio
async def test_get_question_by_id_with_answers(client):
    """Тест получения вопроса с ответами"""
    # Создаем вопрос
    create_response = await client.post(
        "/api/v1/questions/",
        json={"text": "Вопрос с ответами"}
    )
    question_id = create_response.json()["data"]["id"]

    # Создаем ответы
    await client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={"text": "Ответ 1", "user_id": 1}
    )
    await client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={"text": "Ответ 2", "user_id": 2}
    )

    # Получаем вопрос
    response = await client.get(f"/api/v1/questions/{question_id}")

    assert response.status_code == status.HTTP_200_OK
    question = response.json()["data"]

    assert len(question["answers"]) == 2
    assert all("id" in answer for answer in question["answers"])
    assert all("text" in answer for answer in question["answers"])
    assert all("user_id" in answer for answer in question["answers"])


@pytest.mark.asyncio
async def test_get_nonexistent_question(client):
    """Тест получения несуществующего вопроса"""
    response = await client.get("/api/v1/questions/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_data = response.json()
    assert "message" in response_data
    assert "data" in response_data
    assert response_data["data"] is None
    assert "not found" in response_data["message"]


@pytest.mark.asyncio
async def test_get_question_invalid_id(client):
    """Тест получения вопроса с невалидным ID"""
    response = await client.get("/api/v1/questions/abc")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_data = response.json()
    assert "message" in response_data
    assert "data" in response_data
    assert "Validation error" in response_data["message"]


@pytest.mark.asyncio
async def test_delete_question_success(client):
    """Тест успешного удаления вопроса"""
    # Создаем вопрос
    create_response = await client.post(
        "/api/v1/questions/",
        json={"text": "Вопрос для удаления"}
    )
    question_id = create_response.json()["data"]["id"]

    # Удаляем вопрос
    response = await client.delete(f"/api/v1/questions/{question_id}")

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert "message" in response_data
    assert "data" in response_data
    assert response_data["message"] == "Question deleted successfully"
    assert response_data["data"]["id"] == question_id

    # Проверяем, что вопрос удален
    get_response = await client.get(f"/api/v1/questions/{question_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_question_cascade_answers(client, db_session):
    """Тест каскадного удаления ответов при удалении вопроса"""
    from app.domains.answers.model import Answer
    from sqlalchemy import select

    # Создаем вопрос
    create_response = await client.post(
        "/api/v1/questions/",
        json={"text": "Вопрос с ответами"}
    )
    question_id = create_response.json()["data"]["id"]

    # Создаем ответы
    answer1_response = await client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={"text": "Ответ 1", "user_id": 1}
    )
    answer1_id = answer1_response.json()["data"]["id"]

    answer2_response = await client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={"text": "Ответ 2", "user_id": 2}
    )
    answer2_id = answer2_response.json()["data"]["id"]

    # Удаляем вопрос
    await client.delete(f"/api/v1/questions/{question_id}")

    # Обновляем сессию, чтобы увидеть изменения в БД
    await db_session.commit()

    # Проверяем, что ответы удалены из базы данных
    result1 = await db_session.execute(select(Answer).filter(Answer.id == answer1_id))
    answer1 = result1.scalar_one_or_none()
    assert answer1 is None, "Ответ 1 должен быть удален"

    result2 = await db_session.execute(select(Answer).filter(Answer.id == answer2_id))
    answer2 = result2.scalar_one_or_none()
    assert answer2 is None, "Ответ 2 должен быть удален"


@pytest.mark.asyncio
async def test_delete_nonexistent_question(client):
    """Тест удаления несуществующего вопроса"""
    response = await client.delete("/api/v1/questions/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_data = response.json()
    assert "message" in response_data
    assert "data" in response_data
    assert response_data["data"] is None
    assert "not found" in response_data["message"]


@pytest.mark.asyncio
async def test_delete_question_invalid_id(client):
    """Тест удаления вопроса с невалидным ID"""
    response = await client.delete("/api/v1/questions/abc")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_data = response.json()
    assert "message" in response_data
    assert "data" in response_data
    assert "Validation error" in response_data["message"]
