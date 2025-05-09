from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class SettingsPage(BasePage):
    # 로케이터 정의
    URL_LINK_INPUT = (By.CSS_SELECTOR,'input[placeholder="URL of profile picture"]')
    LOGOUT_BTN = (By.XPATH, '//button[text()="Or click here to logout."]')



    def __init__(self, driver):
        super().__init__(driver)

    def click_logout_btn(self):
        self.click_element(self.LOGOUT_BTN)