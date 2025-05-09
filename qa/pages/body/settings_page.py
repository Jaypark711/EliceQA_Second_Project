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

    