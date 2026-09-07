from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    ENTRY_BUTTON = (By.CSS_SELECTOR, ".sign-in-button")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[type='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    LOGIN_BUTTON = (By.XPATH, "//*[@role='button' and contains(., 'Войти')]")

    def login(self, email: str, password: str) -> None:
        self.click(self.ENTRY_BUTTON)
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
