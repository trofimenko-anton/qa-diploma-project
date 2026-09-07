import allure
import pytest
from config.settings import API_URL


@allure.feature("API")
@allure.story("Управление задачами")
@pytest.mark.api
class TestTasksAPI:

    @allure.title("Получение списка досок")
    def test_get_boards(self, api_client) -> None:
        url = f"{API_URL}/boards"
        with allure.step(f"Отправить GET запрос на {url}"):
            response = api_client.get(url)
        with allure.step("Проверить статус-код 200"):
            assert response.status_code == 200
        with allure.step(
                "Проверить, что в ответе есть поле content "
                "и оно является списком"):
            data = response.json()
            assert "content" in data, (
                "В ответе отсутствует поле 'content'"
            )
            assert isinstance(data["content"], list), (
                "Поле 'content' не является списком"
            )

    @allure.title("Создание задачи")
    def test_create_task(self, api_client, column_id) -> None:
        url = f"{API_URL}/tasks"
        payload = {"title": "Новая задача API", "columnId": column_id}
        with allure.step(
                f"Отправить POST запрос на {url} с телом {payload}"):
            response = api_client.post(url, json=payload)
        with allure.step("Проверить статус-код 200 или 201"):
            assert response.status_code in [200, 201]
        with allure.step("Проверить, что в ответе есть ID задачи"):
            task_id = response.json().get("id")
            assert task_id is not None
            allure.attach(
                str(task_id),
                "task_id",
                allure.attachment_type.TEXT
            )

    @allure.title("Обновление задачи")
    def test_update_task(self, api_client, column_id) -> None:
        # Создаём задачу, чтобы получить её id
        create_payload = {"title": "Старое название", "columnId": column_id}
        create_response = api_client.post(
            f"{API_URL}/tasks", json=create_payload
        )
        assert create_response.status_code in [200, 201], (
            f"Не удалось создать задачу: "
            f"{create_response.status_code}, {create_response.text}"
        )
        task_id = create_response.json()["id"]

        # Обновляем задачу
        update_payload = {"title": "Обновлённое название"}
        with allure.step(f"Отправить PUT запрос на /tasks/{task_id}"):
            update_response = api_client.put(
                f"{API_URL}/tasks/{task_id}",
                json=update_payload
            )
        with allure.step("Проверить статус-код 200"):
            assert update_response.status_code == 200
        with allure.step("Проверить, что в ответе есть id задачи"):
            update_data = update_response.json()
            assert "id" in update_data, (
                "В ответе отсутствует поле 'id'"
            )
            assert update_data["id"] == task_id, (
                "ID задачи в ответе не совпадает"
            )

        # Дополнительно проверяем, что задача действительно обновилась,
        # так как PUT /tasks/{id} возвращает только id, а не полный объект
        with allure.step(
                "Получить задачу и убедиться, что title обновился"):
            get_response = api_client.get(f"{API_URL}/tasks/{task_id}")
            assert get_response.status_code == 200, (
                f"Не удалось получить задачу: "
                f"{get_response.status_code}, {get_response.text}"
            )
            assert get_response.json()["title"] == "Обновлённое название", (
                "Название задачи не обновилось: "
                f"{get_response.json().get('title')}"
            )

    @allure.title("Создание задачи без title (негативный)")
    def test_create_task_missing_title(self, api_client, column_id) -> None:
        url = f"{API_URL}/tasks"
        payload = {"columnId": column_id}
        with allure.step("Отправить POST запрос без title"):
            response = api_client.post(url, json=payload)
        with allure.step("Проверить статус-код 400"):
            assert response.status_code == 400

    @allure.title("Получение несуществующей задачи (негативный)")
    def test_get_nonexistent_task(self, api_client) -> None:
        url = f"{API_URL}/tasks/00000000"
        with allure.step(f"Отправить GET запрос на {url}"):
            response = api_client.get(url)
        with allure.step("Проверить статус-код 404"):
            assert response.status_code == 404
