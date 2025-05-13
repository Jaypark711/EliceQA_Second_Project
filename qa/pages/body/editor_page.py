import re
from utils.helpers import Helpers
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait


class EditorPage(BasePage):
    # 로케이터 정의의
    ARTICLE_TITLE_INPUT = (By.CSS_SELECTOR, 'input[placeholder*="Article Title"]')
    ARTICLE_DESCRIPTION_INPUT = (
        By.CSS_SELECTOR,
        'input[placeholder*="What\'s this article about?"]',
    )
    EMPTY_TEXT_DIV = (By.XPATH, '//div[text() = "No articles are here... yet."]')
    ARTICLE_BODY_TEXTAREA = (
        By.CSS_SELECTOR,
        'textarea[placeholder*="Write your article (in markdown)"]',
    )
    ARTICLE_TAG_INPUT = (By.CSS_SELECTOR, 'input[placeholder*="Enter tags"]')
    ARTICLE_TAG_LIST_SPAN = (By.CSS_SELECTOR, 'div span[class*="tag-default"]')
    TAG_DEL_I = (By.CSS_SELECTOR, "i.ion-close-round")
    PUBLISH_BTN = (By.CSS_SELECTOR, "button")

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

    def delete_selected_tags(self, tag_names):
        for tag_name in tag_names:
            # 루프 시마다 태그 요소 리스트 & 태그 삭제 버튼 리스트 불러오기
            article_tag_element_list = self.find_elements(self.ARTICLE_TAG_LIST_SPAN)
            tag_del_btns = self.find_elements(self.TAG_DEL_I)

            # 현재 태그 요소 리스트의 텍스트 값만 추출하여 리스트로 저장
            tag_text_list = []
            for elem in article_tag_element_list:
                tag_text_list.append(elem.text)

            # 태그 요소 텍스트 리스트에서 tag_name과 동일한 값의 index 값 찾기
            del_index = tag_text_list.index(tag_name)

            # 태그 삭제 버튼 리스트에서 삭제할 index 값의 요소 선택하여 클릭
            self.click_element(tag_del_btns[del_index])

    def click_publish_btn(self):
        self.click_element(self.PUBLISH_BTN)

    def save_article(self, title, description, body, tags):
        self.send_article_title(title)
        self.send_article_description(description)
        self.send_article_body(body)
        self.save_article_tags(tags)
        self.click_publish_btn()
