from selenium.webdriver.common.by import By

from pages.base_page import BasePage

class ProfilePage(BasePage):
    # 로케이터 정의
    PROFILE_IMG = (By.CLASS_NAME, 'user-img')
    USERNAME_TITLE = (By.TAG_NAME, 'h4')
    BIO_P = (By.CSS_SELECTOR, 'h4 + p')
    EDIT_PROFILE_SETTINGS_BTN = (By.CSS_SELECTOR, 'a[href="/settings"]')
    MY_ARTICLE_TAB_LINK = (By.XPATH, '//a[text() = "My Articles"]')
    MY_FAVORITED_TAB_LINK = (By.XPATH, '//a[text() = "Favorited Articles"]')

    def __init__(self, driver):
        super().__init__(driver)

    def click_edit_profile_settings_btn(self):
        self.click_element(self.EDIT_PROFILE_SETTINGS_BTN)

    def click_article_tab_link(self):
        self.click_element(self.MY_ARTICLE_TAB_LINK)

    def click_my_favorited_tab_link(self):
        self.click_element(self.MY_FAVORITED_TAB_LINK)