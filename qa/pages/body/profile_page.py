from selenium.webdriver.common.by import By

from config.config import MY_PROFILE_URL, SETTINGS_URL
from pages.base_page import BasePage

class ProfilePage(BasePage):
    # 로케이터 정의
    PROFILE_IMG = (By.CLASS_NAME, 'user-img')
    USERNAME_TITLE = (By.TAG_NAME, 'h4')
    BIO_P = (By.CSS_SELECTOR, 'h4 + p')
    EDIT_PROFILE_SETTINGS_BTN = (By.CSS_SELECTOR, 'a[href="/settings"]')
    MY_ARTICLE_TAB_LINK = (By.XPATH, '//a[text() = "My Articles"]')
    FAVORITED_ARTICLE_TAB_LINK = (By.XPATH, '//a[text() = "Favorited Articles"]')

    def __init__(self, driver):
        super().__init__(driver)

    def click_edit_profile_settings_btn(self):
        self.click_element(self.EDIT_PROFILE_SETTINGS_BTN)

    def click_my_article_tab_link(self):
        self.click_element(self.MY_ARTICLE_TAB_LINK)

    def click_favorited_article_tab_link(self):
        self.click_element(self.FAVORITED_ARTICLE_TAB_LINK)

    def is_my_article_tab_active(self):
        return self.is_element_active(self.MY_ARTICLE_TAB_LINK)

    def is_favorited_article_tab_active(self):
        return self.is_element_active(self.FAVORITED_ARTICLE_TAB_LINK)
    
    def is_go_to_myprofile_page(self):
        return self.get_current_url() == MY_PROFILE_URL

    def is_go_to_settings_page(self):
        return self.get_current_url() == SETTINGS_URL