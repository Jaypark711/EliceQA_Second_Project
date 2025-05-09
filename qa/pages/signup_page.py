from selenium.webdriver.common.by import By

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

    def click_sign_in_btn(self):
        self.click_element(self.SIGN_UP_BTN)

    def sign_up(self, username, email, password):
        self.send_username_input(username)
        self.send_email_input(email)
        self.send_password_input(password)
        self.click_sign_in_btn()