from selenium.webdriver.common.by import By

from pages.base_page import BasePage

class ArticleTabComponent(BasePage):
    YOUR_FEED_TAB_LINK = (By.XPATH, '//a[text()="Your Feed"]')
    GLOBAL_FEED_TAB_LINK = (By.XPATH, '//a[text()="Global Feed"]')

    def __init__(self, driver):
        super().__init__(driver)

    def is_your_feed_tab_link_appear(self):
        return self.is_element_appear(self.YOUR_FEED_TAB_LINK)

    def is_your_feed_tab_link_disappear(self):
        return self.is_element_disappear(self.YOUR_FEED_TAB_LINK)

    def click_your_feed_tab_link(self):
        self.click_element(self.YOUR_FEED_TAB_LINK)

    def click_global_feed_tab_link(self):
        self.click_element(self.GLOBAL_FEED_TAB_LINK)