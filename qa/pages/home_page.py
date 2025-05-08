from selenium.webdriver.common.by import By

from qa.pages.base_page import BasePage

class HomePage(BasePage):
    # 로케이터 정의
    SIGN_IN_LINK = (By.XPATH, "//a[@href='/login']")

    def __init__(self, driver):
        super().__init__(driver)

    def click_sign_in_link(self):
        self.click_element(self.SIGN_IN_LINK)