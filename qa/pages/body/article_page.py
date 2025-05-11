from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement


class ArticlePage(BasePage):
    # 로케이터 정의
    # Article 목록 관련 로케이터
    ARTICLE_PREVIEW_DIV = (By.CSS_SELECTOR, 'div.article-preview')
    ARTICLE_PREVIEW_USERNAME_ = (By.CSS_SELECTOR, "a.author")
    ARTICLE_PREVIEW_TITLE_H1 = (By.CSS_SELECTOR, "a.preview-link > h1")
    ARTICLE_PREVIEW_BODY_P = (By.CSS_SELECTOR, "div.article-preview")
    ARTICLE_PREVIEW_TAGS_UL = (By.CSS_SELECTOR, "ul.tag-list")
    ARTICLE_PREVIEW_TAGS_LI = (By.TAG_NAME, "li")

    # New Post 페이지 관련 로케이터
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
    ARTICLE_TAG_LIST_SPAN = (By.CSS_SELECTOR, 'div span[class*="tag-default"]')
    TAG_DEL_I = (By.TAG_NAME, "i")
    PUBLISH_BTN = (By.CSS_SELECTOR, "button")

    def __init__(self, driver):
        super().__init__(driver)

    # 모든 자식 요소 찾기
    def find_child_elements(self, parents_elem: WebElement, child_locator):
        return parents_elem.find_elements(*child_locator)

    def load_article_lists(self):
        # 작성된 게시글이 있는지 여부 판단 (하나라도 있으면 1로 count됨)
        article_count = len(self.find_elements(self.ARTICLE_PREVIEW_DIV))
        articles = {}  # 정제된 articles 데이터를 담을 딕셔너리 변수
        if article_count < 1:
            return None
        else:  # 등록 게시물이 1개 이상 존재하는 경우
            pre_titles = []
            pre_bodies = []
            pre_tags = []

            pre_title_elems = self.find_elements(self.ARTICLE_PREVIEW_TITLE_H1)
            pre_body_elems = self.find_elements(self.ARTICLE_PREVIEW_BODY_P)
            pre_tag_elems = self.find_elements(self.ARTICLE_PREVIEW_TAGS_UL)

            # 게시글 제목 텍스트 값 추출
            for title in pre_title_elems:
                title_text = title.text
                pre_titles.append(title_text)

            # 게시글 본문 텍스트 값 추출
            for body in pre_body_elems:
                # 본문 내용에 글 작성자, 날짜 정보와 read more 부분도 포함되어 필요 내용 외 삭제
                lines = body.text.split("\n")
                body_text = lines[4]
                pre_bodies.append(body_text)

            # 태그 텍스트 추출
            for tag_ul in pre_tag_elems:
                current_article_tags = self.find_child_elements(
                    tag_ul, self.ARTICLE_PREVIEW_TAGS_LI
                )
                if len(current_article_tags) == 0:
                    pre_tags.append("")
                elif len(current_article_tags) == 1:
                    pre_tags.append(current_article_tags[0].text)
                elif len(current_article_tags) >= 2:
                    tag_group_list = []
                    for tag_li in current_article_tags:
                        tag_group_list.append(tag_li.text)
                    pre_tags.append(tag_group_list)

        # 디버깅용
        # print(f"수집된 제목 총{len(pre_titles)}개 - : {pre_titles}\n")
        # print(f"수집된 본문 내용 총{len(pre_bodies)}개 - : {pre_bodies}\n")
        # print(f"수집된 태그 총{len(pre_tags)}개 - : {pre_tags}\n")

        for i in range(len(pre_titles)):
            articles[f"article{i+1}"] = {
                "title": pre_titles[i],
                "body": pre_bodies[i],
                "tags": pre_tags[i],
            }
        # print(articles)   # 디버깅용
        return articles

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

    # 아직 정상 동작하는지 확인하지 못 했음. 작업 이어서 필요
    def delete_selected_tags(self, tag_names):
        for tag_name in tag_names:
            # 루프 시마다 태그 요소 리스트 & 태그 삭제 버튼 리스트 불러오기
            article_tag_element_list = self.find_elements(self.ARTICLE_TAG_LIST_SPAN)
            tag_del_btns = self.find_elements(self.TAG_DEL_I)

            # 현재 태그 요소 리스트의 텍스트 값만 추출하여 리스트로 저장
            tag_text_list = []
            for elem in article_tag_element_list:
                tag_text_list.append(self.get_text(elem))

            # 태그 요소 텍스트 리스트에서 tag_name과 동일한 값의 index 값 찾기
            del_index = tag_text_list.index(tag_name)

            # 태그 삭제 버튼 리스트에서 삭제할 index 값의 요소 선택하여 클릭
            self.click_element(tag_del_btns[del_index])
