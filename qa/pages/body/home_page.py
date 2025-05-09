import random
from selenium.webdriver.common.by import By

from data.user_data import VALID_USER 
from pages.base_page import BasePage

class HomePage(BasePage):
    TAG_TAB_LINK = (By.CSS_SELECTOR, 'a.nav-link.active')
    POPULAR_TAG_LINK = (By.CSS_SELECTOR, 'a.tag-default')

    def __init__(self, driver):
        super().__init__(driver)

    def click_tag_tab_link(self):
        self.click_element(self.TAG_TAB_LINK)

    def click_random_popular_tag_link(self):
        tags = self.find_elements(self.POPULAR_TAG_LINK)
        random_index = random.randint(0, len(tags) - 1)
        self.click_element(tags[random_index])

        return tags[random_index].text

    def get_tag_tab_link_text(self):
        return self.get_text(self.TAG_TAB_LINK)