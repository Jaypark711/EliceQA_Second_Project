import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By

from pages.base_page import BasePage

load_dotenv(dotenv_path="config/.env")

class LoginPage(BasePage):
    # 로케이터 정의
    PAGE_TITLE = (By.XPATH, '//h1[text()="Sign In"]')
    SIGN_UP_LINK = (By.XPATH, '//a[@href="register"]')
    EMAIL_INPUT = (By.CSS_SELECTOR, 'input[type="email"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, 'input[type="password"]')
    SIGN_IN_BTN = (By.XPATH, '//button[@type="submit"]')

    def __init__(self, driver):
        super().__init__(driver)

    def send_email_input(self):
        self.send_keys(self.EMAIL_INPUT, os.getenv("LOGIN_EMAIL"))

    def send_password_input(self):
        self.send_keys(self.PASSWORD_INPUT, os.getenv("LOGIN_PWD"))

    def click_sign_in_btn(self):
        self.click_element(self.SIGN_IN_BTN)

    def login(self):
        self.send_keys(self.EMAIL_INPUT, os.getenv("LOGIN_EMAIL"))
        self.send_keys(self.PASSWORD_INPUT, os.getenv("LOGIN_PWD"))
        self.click_element(self.SIGN_IN_BTN)