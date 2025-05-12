from selenium.webdriver.common.by import By

from pages.base_page import BasePage

class ProfilePage(BasePage):
    # 로케이터 정의
    PROFILE_IMG = (By.CLASS_NAME, 'user-img')
    USERNAME_TITLE = (By.TAG_NAME, 'h4')
    BIO_P = (By.CSS_SELECTOR, 'h4 + p')
    EDIT_PROFILE_SETTINGS_BTN = (By.CSS_SELECTOR, 'a[href="/settings"]')
    MY_ARTICLE_TAB_LINK = (By.XPATH, '//a[text() = "My Articles"]')
    FAVORITED_ARTICLE_TAB_LINK = (By.XPATH, '//a[text() = "Favorited Articles"]')
    EMPTY_TEXT_DIV = (By.XPATH, '//div[text() = "No articles are here... yet."]')

    def __init__(self, driver):
        super().__init__(driver)

    def is_my_article_tab_active(self):
        return self.is_element_active(self.MY_ARTICLE_TAB_LINK)

    def is_favorited_article_tab_active(self):
        return self.is_element_active(self.FAVORITED_ARTICLE_TAB_LINK)
    
    def is_empty_text_div_show(self):
        return self.is_element_appear(self.EMPTY_TEXT_DIV)

    def click_edit_profile_settings_btn(self):
        self.click_element(self.EDIT_PROFILE_SETTINGS_BTN)

    def click_my_article_tab_link(self):
        self.click_element(self.MY_ARTICLE_TAB_LINK)

    def click_favorited_article_tab_link(self):
        self.click_element(self.FAVORITED_ARTICLE_TAB_LINK)

    def get_profile_img_src(self):
        return self.get_attribute(self.PROFILE_IMG, "src")
    
    def get_username_title_text(self):
        return self.get_text(self.USERNAME_TITLE)
    
    def get_bio_p_text(self):
        return self.get_text(self.BIO_P)