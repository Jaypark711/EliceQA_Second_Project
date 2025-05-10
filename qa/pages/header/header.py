from selenium.webdriver.common.by import By

from config.config import BASE_URL, SIGNIN_URL, SIGNUP_URL, SETTINGS_URL, MY_PROFILE_URL
from data.user_data import VALID_USER 
from pages.base_page import BasePage

class Header(BasePage):
    # 공통 로케이터
    HOME_LINK = (By.XPATH, '//a[text()="Home"]')

    # 비로그인 상태 로케이터
    SIGN_IN_LINK = (By.CSS_SELECTOR, 'a[href="/login"]')
    SIGN_UP_LINK = (By.CSS_SELECTOR, 'a[href="/register"]')

    # 로그인 상태 로케이터
    NEW_POST_LINK = (By.CSS_SELECTOR, 'a[href="/editor"]')
    SETTINGS_LINK = (By.CSS_SELECTOR, 'a[href="/settings"]')
    MY_PROFILE_LINK = (By.CSS_SELECTOR, f'a[href="/@{VALID_USER["username"]}"]')

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

    def click_my_profile_link(self):
        self.click_element(self.MY_PROFILE_LINK)
    
    def is_go_to_home_page(self):
        return self.wait_until_url_and_get(BASE_URL) == BASE_URL
    
    def is_go_to_sign_in_page(self):
        return self.wait_until_url_and_get(SIGNIN_URL) == SIGNIN_URL
    
    def is_go_to_sign_up_page(self):
        return self.wait_until_url_and_get(SIGNUP_URL) == SIGNUP_URL

    def is_go_to_settings_page(self):
        return self.wait_until_url_and_get(SETTINGS_URL) == SETTINGS_URL

    def is_go_to_myprofile_page(self):
        return self.wait_until_url_and_get(MY_PROFILE_URL) == MY_PROFILE_URL

    def is_new_post_link_appear(self):
        return self.is_element_appear(self.NEW_POST_LINK)

    def is_settings_link_appear(self):
        return self.is_element_appear(self.SETTINGS_LINK)

    def is_my_profile_link_appear(self):
        return self.is_element_appear(self.MY_PROFILE_LINK)

    def is_new_post_link_disappear(self):
        return self.is_element_disappear(self.NEW_POST_LINK)
    
    def is_settings_link_disappear(self):
        return self.is_element_disappear(self.SETTINGS_LINK)

    def is_my_profile_link_disappear(self):
        return self.is_element_disappear(self.MY_PROFILE_LINK)

    def get_username_link_text(self):
        return self.get_attribute(self.MY_PROFILE_LINK, "href")