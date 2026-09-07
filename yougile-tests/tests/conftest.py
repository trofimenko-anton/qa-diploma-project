import pytest
import allure
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from config.settings import BASE_URL, LOGIN, PASSWORD, TOKEN, API_URL, BROWSER
from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def api_client():
    with allure.step("Создать сессию API с токеном"):
        session = requests.Session()
        session.headers.update({
            "Authorization": f"Bearer {TOKEN}"
        })
        return session


@pytest.fixture(scope="function")
def driver():
    with allure.step("Запустить браузер"):
        if BROWSER.lower() == "chrome":
            options = ChromeOptions()
            driver = webdriver.Chrome(options=options)
        elif BROWSER.lower() == "firefox":
            options = FirefoxOptions()
            driver = webdriver.Firefox(options=options)
        elif BROWSER.lower() == "edge":
            options = EdgeOptions()
            driver = webdriver.Edge(options=options)
        else:
            raise ValueError(f"Unsupported browser: {BROWSER}")
        driver.maximize_window()
    yield driver
    with allure.step("Закрыть браузер"):
        driver.quit()


@pytest.fixture(scope="function")
def logged_in_driver(driver):
    with allure.step("Выполнить вход в систему"):
        login_page = LoginPage(driver)
        login_page.open(BASE_URL)
        login_page.login(LOGIN, PASSWORD)
    return driver


@pytest.fixture(scope="session")
def column_id(api_client):
    with allure.step("Получить ID текущего пользователя"):
        user_response = api_client.get(f"{API_URL}/users/me")
        assert user_response.status_code == 200
        user_id = user_response.json()["id"]

    with allure.step("Создать проект"):
        project_payload = {
            "title": "Проект для диплома",
            "users": {user_id: "admin"}
        }
        project_response = api_client.post(
            f"{API_URL}/projects", json=project_payload
        )
        assert project_response.status_code in [200, 201]
        project_id = project_response.json()["id"]

    with allure.step("Создать доску"):
        board_payload = {
            "title": "Тестовая доска",
            "projectId": project_id,
            "stickers": {
                "timer": False,
                "deadline": True,
                "stopwatch": True,
                "timeTracking": True,
                "assignee": True,
                "repeat": True
            }
        }
        board_response = api_client.post(
            f"{API_URL}/boards", json=board_payload
        )
        assert board_response.status_code in [200, 201]
        board_id = board_response.json()["id"]

    with allure.step("Создать колонку"):
        column_payload = {
            "title": "To Do",
            "color": 10,
            "boardId": board_id
        }
        column_response = api_client.post(
            f"{API_URL}/columns", json=column_payload
        )
        assert column_response.status_code in [200, 201]
        col_id = column_response.json()["id"]

    return col_id
