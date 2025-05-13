from selenium.webdriver.common.by import By

from pages.base_page import BasePage

class ProfileComponent(BasePage):
    # 로케이터 정의
    PROFILE_IMG = (By.CLASS_NAME, 'user-img')
    USERNAME_TITLE = (By.TAG_NAME, 'h4')
    BIO_P = (By.CSS_SELECTOR, 'h4 + p')
    EDIT_PROFILE_SETTINGS_BTN = (By.CSS_SELECTOR, 'a[href="/settings"]')
    MY_ARTICLE_TAB_LINK = (By.XPATH, '//a[text() = "My Articles"]')
    FAVORITED_ARTICLE_TAB_LINK = (By.XPATH, '//a[text() = "Favorited Articles"]')
    FOLLOW_BTN = (By.XPATH, "//button[contains(@class,'action-btn') and contains(., 'Follow')]")
    UNFOLLOW_BTN = (By.XPATH, "//button[contains(@class,'action-btn') and contains(., 'Unfollow')]")

    def __init__(self, driver):
        super().__init__(driver)

    def is_my_article_tab_active(self):
        return self.is_element_active(self.MY_ARTICLE_TAB_LINK)

    def is_favorited_article_tab_active(self):
        return self.is_element_active(self.FAVORITED_ARTICLE_TAB_LINK)

    def click_edit_profile_settings_btn(self):
        self.click_element(self.EDIT_PROFILE_SETTINGS_BTN)

    def click_my_article_tab_link(self):
        self.click_element(self.MY_ARTICLE_TAB_LINK)

    def click_favorited_article_tab_link(self):
        self.click_element(self.FAVORITED_ARTICLE_TAB_LINK)

    def click_follow_btn(self):
        self.click_element(self.FOLLOW_BTN)
    
    def click_unfollow_btn(self):
        self.click_element(self.UNFOLLOW_BTN)    

    def get_profile_img_src(self):
        return self.get_attribute(self.PROFILE_IMG, "src")
    
    def get_username_title_text(self):
        return self.get_text(self.USERNAME_TITLE)
    
    def get_bio_p_text(self):
        return self.get_text(self.BIO_P)