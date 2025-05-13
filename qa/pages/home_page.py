from pages.base_page import BasePage
from components.header.header_component import HeaderComponent
from components.body.article_tab_component import ArticleTabComponent
from components.body.popular_tags_component import PopularTagsComponent
from components.body.article_component import ArticleComponent

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.header = HeaderComponent(driver)
        self.tabs = ArticleTabComponent(driver)
        self.popular_tags = PopularTagsComponent(driver)
        self.article = ArticleComponent(driver)