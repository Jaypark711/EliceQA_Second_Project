from selenium.webdriver.common.by import By

from data.user_data import VALID_USER 
from pages.base_page import BasePage

class HomePage(BasePage):
    # 공통 로케이터
    HOME_LINK = (By.XPATH, '//a[text()="Home"]')

    # 비로그인 상태 로케이터
    SIGN_IN_LINK = (By.CSS_SELECTOR, 'a[href="/login"]')
    SIGN_UP_LINK = (By.CSS_SELECTOR, 'a[href="/register"]')

    # 로그인 상태 로케이터
    NEW_POST_LINK = (By.CSS_SELECTOR, 'a[href="/editor"]')
    SETTINGS_LINK = (By.CSS_SELECTOR, 'a[href="/settings"]')
    USER_PROFILE_LINK = (By.CSS_SELECTOR, f'a[href="/@{VALID_USER["username"]}"]')

    def __init__(self, driver):
        super().__init__(driver)

    def click_home_link(self):
        self.click_element(self.HOME_LINK)

    def click_sign_in_link(self):
        self.click_element(self.SIGN_IN_LINK)

    def click_sign_up_link(self):
        self.click_element(self.SIGN_UP_LINK)

    def click_new_post_link(self):
        self.click_element(self.NEW_POST_LINK)

    def click_settings_link(self):
        self.click_element(self.SETTINGS_LINK)

    def wait_for_user_profile_link(self):
        self.find_element(self.USER_PROFILE_LINK)

    def get_username_link_text(self):
        href = self.get_attribute(self.USER_PROFILE_LINK, "href")