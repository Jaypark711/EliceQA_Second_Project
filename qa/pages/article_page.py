from pages.base_page import BasePage
from pages.home_page import HomePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class ArticlePage(BasePage):
    # 로케이터 정의
    ARTICLE_TITLE_INPUT = (By.CSS_SELECTOR, 'input[placeholder*="Article Title"]')
    ARTICLE_DESCRIPTION_INPUT = (
        By.CSS_SELECTOR,
        'input[placeholder*="What\'s this article about?"]',
    )
    ARTICLE_BODY_TEXTAREA = (
        By.CSS_SELECTOR,
        'textarea[placeholder*="Write your article (in markdown)"]',
    )
    ARTICLE_TAG_INPUT = (By.CSS_SELECTOR, 'input[placeholder*="Enter tags"]')

    PUBLISH_BTN = (By.CSS_SELECTOR, 'button')
    # ARTICLE_TAG_DELETE_ICONS = (By.CLASS_NAME, 'ion-close-round') - 태그 삭제는 우선 게시글 등록 함수 만들고 나서 개발 예정




    def __init__(self, driver):
        super().__init__(driver)

    def send_article_title(self, title):
        self.send_keys(self.ARTICLE_TITLE_INPUT, title)

    def send_article_description(self, description):
        self.send_keys(self.ARTICLE_DESCRIPTION_INPUT, description)

    def send_article_body(self, body):
        self.send_keys(self.ARTICLE_BODY_TEXTAREA, body)

    def save_article_tags(self, tags):
        for tag in tags:
            self.send_keys(self.ARTICLE_TAG_INPUT, tag)
            self.send_keys(self.ARTICLE_TAG_INPUT, Keys.ENTER)

    def click_publish_btn(self):
        self.click_element(self.PUBLISH_BTN)

    def save_article(self, title, description, body, tags):
        self.send_article_title(title)
        self.send_article_description(description)
        self.send_article_body(body)
        self.save_article_tags(tags)
        self.click_publish_btn()


    # def delete_artigle_tag(self,indexes):
    #     pass
