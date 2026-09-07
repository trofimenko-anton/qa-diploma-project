from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
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
    PROJECTS_LIST = (
        By.CSS_SELECTOR,
        "[data-testid='projects-list']"
    )

    def _project_locator(self, title: str):
        return (
            By.XPATH,
            f"//div[@data-testid='projects-list']"
            f"//div[@data-testid='project-item']"
            f"//div[contains(@class, 'truncate') "
            f"and normalize-space()='{title}']"
        )

    def create_project(self, title: str) -> None:
        self.click_js(self.ADD_PROJECT_BUTTON)
        self.click_js(self.PROJECT_WITH_TASKS)
        self.type_text(self.PROJECT_NAME_INPUT, title)
        self.click_js(self.CONFIRM_PROJECT_BUTTON)

        # Ждём, пока созданный проект появится в списке проектов
        self.wait.until(
            EC.visibility_of_element_located(self._project_locator(title))
        )

    def is_project_present(self, title: str) -> bool:
        try:
            self.wait.until(
                EC.visibility_of_element_located(self._project_locator(title))
            )
            return True
        except TimeoutException:
            return False

    def open_first_board(self) -> None:
        self.wait.until(EC.visibility_of_element_located(self.PROJECT_CARD))
        self.click(self.PROJECT_CARD)
