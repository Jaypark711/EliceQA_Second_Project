from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class SettingsPage(BasePage):
    # 로케이터 정의
    PAGE_TITLE = (By.XPATH, '//h1[text()="Your Settings"]')
    URL_LINK_INPUT = (By.CSS_SELECTOR,'input[placeholder="URL of profile picture"]')
    USERNAME_INPUT = (By.CSS_SELECTOR,'input[placeholder="Username"]')
    BIO_INPUT = (By.CSS_SELECTOR,'textarea[placeholder="Short bio about you"]')
    EMAIL_INPUT = (By.CSS_SELECTOR,'input[placeholder="Email"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR,'input[placeholder="New Password"]')
    UPDATE_BTN = (By.CSS_SELECTOR, 'button[type="submit"]')
    LOGOUT_BTN = (By.XPATH, '//button[text()="Or click here to logout."]')

    def __init__(self, driver):
        super().__init__(driver)
    
    def send_url_link_input(self, url):
        self.send_keys(self.URL_LINK_INPUT, url)

    def send_username_input(self, username):
        self.send_keys(self.USERNAME_INPUT, username)
    
    def send_bio_input(self, bio):
        self.send_keys(self.BIO_INPUT, bio)
    
    def send_email_input(self, email):
        self.send_keys(self.EMAIL_INPUT, email)
    
    def send_password_input(self, password):
        self.send_keys(self.PASSWORD_INPUT, password)
    
    def click_logout_btn(self):
        self.click_element(self.LOGOUT_BTN)
    
    def is_value_length_equal(self, locator, expected):
        actual = self.get_attribute(locator, "value")
        return len(actual) == len(expected)
    
    def is_password_length_equal(self, expected):
        return self.is_value_length_equal(self.PASSWORD_INPUT,expected)
    
    def click_update_btn(self):
        self.click_element(self.UPDATE_BTN)

    def get_url_link_input_value(self):
        return self.get_attribute(self.URL_LINK_INPUT, "value")
    
    def get_username_input_value(self):
        return self.get_attribute(self.USERNAME_INPUT, "value")
    
    def get_bio_input_value(self):
        return self.get_attribute(self.BIO_INPUT, "value")
    
    def get_email_input_value(self):
        return self.get_attribute(self.EMAIL_INPUT, "value")
    
    def get_password_input_value(self):
        return self.get_attribute(self.PASSWORD_INPUT, "value")

    def change_user_info(self, **kwargs):
    # 키와 메서드 매핑 테이블
        actions = {
            "url": self.send_url_link_input,
            "username": self.send_username_input,
            "bio": self.send_bio_input,
            "email": self.send_email_input,
            "password": self.send_password_input,
        }

        for key, func in actions.items():
            if key in kwargs and kwargs[key] is not None:
                func(kwargs[key])