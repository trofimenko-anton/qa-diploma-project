from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class BoardsPage(BasePage):
    ADD_PROJECT_BUTTON = (
        By.XPATH,
        "//div[@data-testid='panel-company-projects']"
        "//span[normalize-space()='Добавить проект']"
    )
    PROJECT_WITH_TASKS = (
        By.CSS_SELECTOR,
        "[data-testid='menu-item-add-default-project']"
    )
    PROJECT_NAME_INPUT = (
        By.CSS_SELECTOR,
        "input[placeholder='Введите название проекта…']"
    )
    CONFIRM_PROJECT_BUTTON = (
        By.XPATH,
        "//*[@role='button' and "
        "contains(., 'Добавить проект с задачами')]"
    )
    PROJECT_CARD = (By.CSS_SELECTOR, "[data-testid='project-card']")
    CREATE_COLUMN_BUTTON = (
        By.XPATH,
        "//div[@role='button' and "
        ".//span[normalize-space()='Создать колонку']]"
    )

    def create_project(self, title: str) -> None:
        self.click_js(self.ADD_PROJECT_BUTTON)
        self.click_js(self.PROJECT_WITH_TASKS)
        self.type_text(self.PROJECT_NAME_INPUT, title)
        self.click_js(self.CONFIRM_PROJECT_BUTTON)
        self.wait.until(
            EC.visibility_of_element_located(self.CREATE_COLUMN_BUTTON)
        )

    def open_first_board(self) -> None:
        self.wait.until(
            EC.visibility_of_element_located(self.PROJECT_CARD)
        )
        self.click(self.PROJECT_CARD)

    def is_board_present(self, title: str) -> bool:
        locator = (
            By.XPATH,
            f"//*[@data-testid='project-card' "
            f"and contains(., '{title}')]"
        )
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False
