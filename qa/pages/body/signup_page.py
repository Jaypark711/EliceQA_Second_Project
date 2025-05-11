from selenium.webdriver.common.by import By

from data.user_data import VALID_USER
from pages.base_page import BasePage

class SignUpPage(BasePage):
    PAGE_TITLE = (By.XPATH, '//h1[text()="Sign Up"]')
    SIGN_IN_LINK = (By.XPATH, '//a[@href="login"]')
    USERNAME_INPUT = (By.CSS_SELECTOR, 'input[type="text"]')
    EMAIL_INPUT = (By.CSS_SELECTOR, 'input[type="email"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, 'input[type="password"]')
    SIGN_UP_BTN = (By.CSS_SELECTOR, 'button[type="submit"]')

    def __init__(self, driver):
        super().__init__(driver)

    def send_username_input(self, username):
        self.send_keys(self.USERNAME_INPUT, username)

    def send_email_input(self, email):
        self.send_keys(self.EMAIL_INPUT, email)

    def send_password_input(self, password):
        self.send_keys(self.PASSWORD_INPUT, password)

    def click_sign_up_btn(self):
        self.click_element(self.SIGN_UP_BTN)

    def get_username_input_value(self):
        return self.get_attribute(self.USERNAME_INPUT, "value")

    def get_email_input_value(self):
        return self.get_attribute(self.EMAIL_INPUT, "value")
    
    def get_password_input_value(self):
        return self.get_attribute(self.PASSWORD_INPUT, "value")

    def sign_up(self):
        self.send_username_input(VALID_USER["username"])
        self.send_email_input(VALID_USER["email"])
        self.send_password_input(VALID_USER["password"])
        self.click_sign_up_btn()