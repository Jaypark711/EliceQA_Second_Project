from selenium.webdriver.common.by import By

from pages.base_page import BasePage

class HomePage(BasePage):
    # 로케이터 정의
    HOME_LINK = (By.XPATH, "//a[text()='Home']")
    SIGN_IN_LINK = (By.XPATH, "//a[@href='/login']")
    SIGN_UP_LINK = (By.XPATH, "//a[@href='/register']")

    def __init__(self, driver):
        super().__init__(driver)

    def click_home_link(self):
        self.click_element(self.HOME_LINK)

    def click_sign_in_link(self):
        self.click_element(self.SIGN_IN_LINK)

    def click_sign_up_link(self):
        self.click_element(self.SIGN_UP_LINK)