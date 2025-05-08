import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By

from qa.pages.base_page import BasePage

load_dotenv(dotenv_path="qa/config/.env")

class LoginPage(BasePage):
    # 로케이터 정의
    EMAIL_INPUT = (By.XPATH, "//input[@type='email']")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    SIGN_IN_BTN = (By.XPATH, "//button[@type='submit']")

    def __init__(self, driver):
        super().__init__(driver)

    def login(self):
        self.send_keys(self.EMAIL_INPUT, os.getenv("LOGIN_EMAIL"))
        self.send_keys(self.PASSWORD_INPUT, os.getenv("LOGIN_PWD"))
        self.click_element(self.SIGN_IN_BTN)