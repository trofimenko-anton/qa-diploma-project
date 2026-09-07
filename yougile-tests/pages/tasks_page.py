from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class TasksPage(BasePage):
    ADD_TASK_BUTTON = (
        By.XPATH,
        "//*[contains(text(), 'Добавить задачу')]"
    )

    TASK_TITLE_INPUT = (
        By.CSS_SELECTOR,
        "[data-testid='board-task-input-name']"
    )

    TASK_CARD = (
        By.CSS_SELECTOR,
        "[data-testid='board-task-card']"
    )

    SEARCH_INPUT = (
        By.CSS_SELECTOR,
        "input[placeholder='Поиск']"
    )

    TASK_MENU_BUTTON = (
        By.CSS_SELECTOR,
        "[data-testid='board-task-menu']"
    )

    RENAME_BUTTON = (
        By.XPATH,
        "//div[normalize-space()='Переименовать']"
    )

    def add_task(self, title: str) -> None:
        self.click_js(self.ADD_TASK_BUTTON)
        self.type_text(self.TASK_TITLE_INPUT, title)
        self.driver.find_element(
            *self.TASK_TITLE_INPUT
        ).send_keys(Keys.ENTER)

    def is_task_present(self, title: str) -> bool:
        locator = (
            By.XPATH,
            f"//*[@data-testid='board-task-card' and contains(., '{title}')]"
        )

        try:
            self.wait.until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except Exception:
            return False

    def is_task_title_present(self, title: str) -> bool:
        locator = (
            By.XPATH,
            f'//div[@data-testid="board-task-title" and '
            f'.//span[normalize-space()="{title}"]]'
        )

        try:
            self.wait.until(
                EC.presence_of_element_located(locator)
            )
            return True
        except Exception:
            return False

    def open_task(self, title: str) -> None:
        locator = (
            By.XPATH,
            f"//*[@data-testid='board-task-card' and contains(., '{title}')]"
        )
        self.click_js(locator)

    def is_task_panel_opened(self) -> bool:
        locator = (
            By.XPATH,
            "//*[@data-testid='right-pane-header']"
        )

        try:
            self.wait.until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except Exception:
            return False

    def edit_task_title(self, old_title: str, new_title: str) -> None:
        # 1. Находим заголовок задачи
        title_element = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    f'//div[@data-testid="board-task-title" and '
                    f'.//span[normalize-space()="{old_title}"]]'
                )
            )
        )

        # 2. Наводим курсор на заголовок
        ActionChains(self.driver).move_to_element(
            title_element
        ).perform()

        # 3. Нажимаем на кнопку "три точки"
        menu_button = self.wait.until(
            EC.element_to_be_clickable(
                self.TASK_MENU_BUTTON
            )
        )
        menu_button.click()

        # 4. Нажимаем "Переименовать"
        rename_button = self.wait.until(
            EC.element_to_be_clickable(
                self.RENAME_BUTTON
            )
        )
        rename_button.click()

        # 5. После "Переименовать" появляется textarea
        edit_input = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "textarea"
                )
            )
        )

        # 6. Выделяем старое название
        edit_input.click()
        edit_input.send_keys(Keys.CONTROL, "a")

        # 7. Вводим новое название
        edit_input.send_keys(new_title)

        # 8. Сохраняем через Enter
        edit_input.send_keys(Keys.ENTER)

        # 9. Ждём, пока новое название появится на странице
        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    f'//div[@data-testid="board-task-title" and '
                    f'.//span[normalize-space()="{new_title}"]]'
                )
            )
        )

    def search(self, query: str) -> None:
        search_input = self.wait.until(
            EC.presence_of_element_located(
                self.SEARCH_INPUT
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            search_input
        )

        self.driver.execute_script(
            "arguments[0].value = arguments[1];",
            search_input,
            query
        )

        self.driver.execute_script(
            """
            arguments[0].dispatchEvent(
                new KeyboardEvent('keydown', {
                    key: 'Enter',
                    keyCode: 13,
                    which: 13
                })
            );
            """,
            search_input
        )
