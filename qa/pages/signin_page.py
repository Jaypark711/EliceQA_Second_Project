from selenium.webdriver.common.by import By

from data.user_data import VALID_USER
from pages.base_page import BasePage

class SignInPage(BasePage):
    # 로케이터 정의
    PAGE_TITLE = (By.XPATH, '//h1[text()="Sign In"]')
    SIGN_UP_LINK = (By.CSS_SELECTOR, 'a[href="register"]')
    EMAIL_INPUT = (By.CSS_SELECTOR, 'input[type="email"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, 'input[type="password"]')
    SIGN_IN_BTN = (By.CSS_SELECTOR, 'button[type="submit"]')

    def __init__(self, driver):
        super().__init__(driver)

    def send_email_input(self, email):
        self.send_keys(self.EMAIL_INPUT, email)

    def send_password_input(self, password):
        self.send_keys(self.PASSWORD_INPUT, password)

    def click_sign_in_btn(self):
        self.click_element(self.SIGN_IN_BTN)

    def login(self):
        self.send_keys(self.EMAIL_INPUT, VALID_USER["email"])
        self.send_keys(self.PASSWORD_INPUT, VALID_USER["password"])
        self.click_element(self.SIGN_IN_BTN)