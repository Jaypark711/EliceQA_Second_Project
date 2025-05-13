from pages.base_page import BasePage
from components.header.header_component import HeaderComponent
from components.body.profile_component import ProfileComponent
from components.body.article_component import ArticleComponent

class ProfilePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.header = HeaderComponent(driver)
        self.profile = ProfileComponent(driver)
        self.article = ArticleComponent(driver)