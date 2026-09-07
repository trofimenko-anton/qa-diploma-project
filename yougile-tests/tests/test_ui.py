import uuid
import allure
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.login_page import LoginPage
from pages.boards_page import BoardsPage
from pages.tasks_page import TasksPage
from config.settings import BASE_URL, LOGIN, PASSWORD


@allure.feature("UI")
@allure.story("Управление досками и задачами")
@pytest.mark.ui
class TestUI:

    @allure.title("Авторизация с валидными данными")
    def test_login(self, driver):
        login_page = LoginPage(driver)
        with allure.step("Открыть главную страницу"):
            login_page.open(BASE_URL)
        with allure.step("Нажать кнопку Войти, ввести данные и войти"):
            login_page.login(LOGIN, PASSWORD)
        with allure.step("Проверить, что мы авторизованы"):
            assert "yougile" in driver.current_url

    @allure.title("Создание нового проекта")
    def test_create_project(self, logged_in_driver):
        boards_page = BoardsPage(logged_in_driver)
        project_title = f"Проект для UI {uuid.uuid4().hex[:6]}"

        with allure.step(f"Создать проект '{project_title}'"):
            boards_page.create_project(project_title)

        with allure.step("Обновить страницу"):
            logged_in_driver.refresh()

        with allure.step("Дождаться загрузки списка проектов"):
            WebDriverWait(logged_in_driver, 10).until(
                EC.visibility_of_element_located(
                    boards_page.PROJECTS_LIST
                )
            )

        with allure.step(
            f"Проверить, что проект '{project_title}' сохранился"
        ):
            assert boards_page.is_project_present(project_title), (
                f"Проект '{project_title}' "
                "не найден после обновления страницы"
            )

    @allure.title("Добавление задачи в колонку")
    def test_add_task(self, logged_in_driver):
        boards_page = BoardsPage(logged_in_driver)
        project_title = f"Проект для задачи {uuid.uuid4().hex[:6]}"
        with allure.step(f"Создать проект '{project_title}'"):
            boards_page.create_project(project_title)

        tasks_page = TasksPage(logged_in_driver)
        task_title = "Новая задача UI"
        with allure.step(f"Добавить задачу '{task_title}'"):
            tasks_page.add_task(task_title)
        with allure.step("Проверить, что задача отображается"):
            assert tasks_page.is_task_present(task_title)

    @allure.title("Просмотр/редактирование задачи")
    def test_edit_task(self, logged_in_driver):
        boards_page = BoardsPage(logged_in_driver)
        project_title = (
            f"Проект для редактирования "
            f"{uuid.uuid4().hex[:6]}"
        )
        with allure.step(f"Создать проект '{project_title}'"):
            boards_page.create_project(project_title)

        tasks_page = TasksPage(logged_in_driver)
        unique_id = uuid.uuid4().hex[:6]
        old_title = f"Старое название {unique_id}"
        new_title = f"Новое название {unique_id}"

        with allure.step(f"Создать задачу '{old_title}'"):
            tasks_page.add_task(old_title)
        with allure.step("Проверить, что задача создана"):
            assert tasks_page.is_task_present(old_title)
        with allure.step("Открыть карточку задачи"):
            tasks_page.open_task(old_title)
        with allure.step("Проверить, что панель задачи открылась"):
            assert tasks_page.is_task_panel_opened()
        with allure.step(f"Изменить название на '{new_title}'"):
            tasks_page.edit_task_title(old_title, new_title)
        with allure.step("Проверить, что название изменилось"):
            assert tasks_page.is_task_title_present(new_title)

    @allure.title("Поиск задачи по названию")
    def test_search_task(self, logged_in_driver):
        boards_page = BoardsPage(logged_in_driver)
        project_title = f"Проект для поиска {uuid.uuid4().hex[:6]}"
        with allure.step(f"Создать проект '{project_title}'"):
            boards_page.create_project(project_title)

        tasks_page = TasksPage(logged_in_driver)
        task_title = "Подготовить презентацию"
        with allure.step(f"Создать задачу '{task_title}'"):
            tasks_page.add_task(task_title)
            assert tasks_page.is_task_present(task_title)

        with allure.step("Выполнить поиск по слову 'презентация'"):
            tasks_page.search("презентация")

        with allure.step("Проверить, что задача найдена"):
            assert tasks_page.is_task_present(task_title)
