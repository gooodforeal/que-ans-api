import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_create_answer_success(client):
    """Тест успешного создания ответа"""
    # Создаем вопрос
    question_response = await client.post(
        "/api/v1/questions/",
        json={"text": "Какой язык программирования лучше?"}
    )
    question_id = question_response.json()["data"]["id"]

    # Создаем ответ
    answer_text = "Python - отличный выбор!"
    user_id = 123

    response = await client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={
            "text": answer_text,
            "user_id": user_id
        }
    )

    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()

    # Проверяем структуру StandardResponse
    assert "message" in response_data
    assert "data" in response_data
    assert response_data["message"] == "Answer created successfully"

    # Проверяем данные ответа
    answer = response_data["data"]
    assert answer["text"] == answer_text
    assert answer["user_id"] == user_id
    assert answer["question_id"] == question_id
    assert "id" in answer
    assert answer["id"] > 0
    assert "created_at" in answer
    assert "updated_at" in answer


@pytest.mark.asyncio
async def test_create_answer_nonexistent_question(client):
    """Тест создания ответа к несуществующему вопросу"""
    response = await client.post(
        "/api/v1/questions/999/answers/",
        json={
            "text": "Ответ",
            "user_id": 123
        }
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_data = response.json()
    assert "detail" in response_data
    assert "does not exist" in response_data["detail"] or "not found" in response_data["detail"]


@pytest.mark.asyncio
async def test_create_answer_empty_text(client):
    """Тест создания ответа с пустым текстом - должна быть ошибка валидации"""
    # Создаем вопрос
    question_response = await client.post(
        "/api/v1/questions/",
        json={"text": "Вопрос"}
    )
    question_id = question_response.json()["data"]["id"]

    response = await client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={
            "text": "",
            "user_id": 123
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_answer_missing_fields(client):
    """Тест создания ответа без обязательных полей"""
    # Создаем вопрос
    question_response = await client.post(
        "/api/v1/questions/",
        json={"text": "Вопрос"}
    )
    question_id = question_response.json()["data"]["id"]

    # Без text
    response = await client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={"user_id": 123}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Без user_id
    response = await client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={"text": "Ответ"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_answer_invalid_user_id(client):
    """Тест создания ответа с невалидным user_id"""
    # Создаем вопрос
    question_response = await client.post(
        "/api/v1/questions/",
        json={"text": "Вопрос"}
    )
    question_id = question_response.json()["data"]["id"]

    # user_id должен быть > 0
    response = await client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={
            "text": "Ответ",
            "user_id": 0
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Отрицательный user_id
    response = await client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={
            "text": "Ответ",
            "user_id": -1
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_answer_text_too_long(client):
    """Тест создания ответа с текстом превышающим максимальную длину"""
    # Создаем вопрос
    question_response = await client.post(
        "/api/v1/questions/",
        json={"text": "Вопрос"}
    )
    question_id = question_response.json()["data"]["id"]

    long_text = "a" * 10001  # Максимальная длина 10000 символов
    response = await client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={
            "text": long_text,
            "user_id": 123
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_get_answer_success(client):
    """Тест успешного получения ответа по ID"""
    # Создаем вопрос и ответ
    question_response = await client.post(
        "/api/v1/questions/",
        json={"text": "Вопрос"}
    )
    question_id = question_response.json()["data"]["id"]

    answer_text = "Ответ на вопрос"
    user_id = 123

    answer_response = await client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={
            "text": answer_text,
            "user_id": user_id
        }
    )
    answer_id = answer_response.json()["data"]["id"]

    # Получаем ответ
    response = await client.get(f"/api/v1/answers/{answer_id}")

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert "message" in response_data
    assert "data" in response_data
    assert response_data["message"] == "Answer retrieved successfully"

    answer = response_data["data"]
    assert answer["id"] == answer_id
    assert answer["text"] == answer_text
    assert answer["user_id"] == user_id
    assert answer["question_id"] == question_id
    assert "created_at" in answer
    assert "updated_at" in answer


@pytest.mark.asyncio
async def test_get_nonexistent_answer(client):
    """Тест получения несуществующего ответа"""
    response = await client.get("/api/v1/answers/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_data = response.json()
    assert "detail" in response_data
    assert "not found" in response_data["detail"]


@pytest.mark.asyncio
async def test_get_answer_invalid_id(client):
    """Тест получения ответа с невалидным ID"""
    response = await client.get("/api/v1/answers/abc")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_delete_answer_success(client):
    """Тест успешного удаления ответа"""
    # Создаем вопрос и ответ
    question_response = await client.post(
        "/api/v1/questions/",
        json={"text": "Вопрос"}
    )
    question_id = question_response.json()["data"]["id"]

    answer_response = await client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={
            "text": "Ответ",
            "user_id": 123
        }
    )
    answer_id = answer_response.json()["data"]["id"]

    # Удаляем ответ
    response = await client.delete(f"/api/v1/answers/{answer_id}")

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert "message" in response_data
    assert "data" in response_data
    assert response_data["message"] == "Answer deleted successfully"
    assert response_data["data"]["id"] == answer_id

    # Проверяем, что ответ удален
    get_response = await client.get(f"/api/v1/answers/{answer_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_nonexistent_answer(client):
    """Тест удаления несуществующего ответа"""
    response = await client.delete("/api/v1/answers/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_data = response.json()
    assert "detail" in response_data
    assert "not found" in response_data["detail"]


@pytest.mark.asyncio
async def test_delete_answer_invalid_id(client):
    """Тест удаления ответа с невалидным ID"""
    response = await client.delete("/api/v1/answers/abc")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_cascade_delete_answers_on_question_delete(client, db_session):
    """Тест каскадного удаления ответов при удалении вопроса"""
    from app.domains.answers.model import Answer
    from sqlalchemy import select

    # Создаем вопрос
    question_response = await client.post(
        "/api/v1/questions/",
        json={"text": "Вопрос"}
    )
    question_id = question_response.json()["data"]["id"]

    # Создаем несколько ответов
    answer1_response = await client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={
            "text": "Ответ 1",
            "user_id": 1
        }
    )
    answer1_id = answer1_response.json()["data"]["id"]

    answer2_response = await client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={
            "text": "Ответ 2",
            "user_id": 2
        }
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
async def test_multiple_answers_from_different_users(client):
    """Тест создания нескольких ответов от разных пользователей"""
    # Создаем вопрос
    question_response = await client.post(
        "/api/v1/questions/",
        json={"text": "Вопрос"}
    )
    question_id = question_response.json()["data"]["id"]

    # Создаем ответы от разных пользователей
    answer1_response = await client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={
            "text": "Ответ от пользователя 1",
            "user_id": 1
        }
    )
    assert answer1_response.status_code == status.HTTP_201_CREATED

    answer2_response = await client.post(
        f"/api/v1/questions/{question_id}/answers/",
        json={
            "text": "Ответ от пользователя 2",
            "user_id": 2
        }
    )
    assert answer2_response.status_code == status.HTTP_201_CREATED

    # Проверяем, что оба ответа созданы
    question_response = await client.get(f"/api/v1/questions/{question_id}")
    question = question_response.json()["data"]
    assert len(question["answers"]) == 2


@pytest.mark.asyncio
async def test_get_question_with_multiple_answers(client):
    """Тест получения вопроса с несколькими ответами"""
    # Создаем вопрос
    question_response = await client.post(
        "/api/v1/questions/",
        json={"text": "Вопрос с несколькими ответами"}
    )
    question_id = question_response.json()["data"]["id"]

    # Создаем несколько ответов
    for i in range(3):
        await client.post(
            f"/api/v1/questions/{question_id}/answers/",
            json={
                "text": f"Ответ {i + 1}",
                "user_id": i + 1
            }
        )

    # Получаем вопрос
    response = await client.get(f"/api/v1/questions/{question_id}")

    assert response.status_code == status.HTTP_200_OK
    question = response.json()["data"]

    assert len(question["answers"]) == 3
    assert all(answer["question_id"] == question_id for answer in question["answers"])
