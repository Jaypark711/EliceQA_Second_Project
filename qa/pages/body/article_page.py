import re
from utils.helpers import Helpers
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait


class ArticlePage(BasePage):
    # 로케이터 정의
    # 공통 로케이터
    TAGS_UL = (By.CSS_SELECTOR, "ul.tag-list")
    TAGS_LI = (By.TAG_NAME, "li")

    # Article 목록 관련 로케이터
    ARTICLE_PREVIEW_DIV = (By.CSS_SELECTOR, "div.article-preview")
    ARTICLE_PREVIEW_DATE = (By.CSS_SELECTOR, "span.date")
    ARTICLE_PREVIEW_PROFILE_IMG = (By.CSS_SELECTOR, "a img")
    ARTICLE_PREVIEW_USERNAME = (By.CSS_SELECTOR, "a.author")
    ARTICLE_PREVIEW_FAVOR_BTN = (By.CSS_SELECTOR, "button:has(> i.ion-heart)")
    ARTICLE_PREVIEW_TITLE_H1 = (By.CSS_SELECTOR, "a.preview-link > h1")
    ARTICLE_PREVIEW_DESCRIPTION_P = (By.CSS_SELECTOR, "div.article-preview")
    ARTICLE_PREVIEW_READMORE_A = (By.CSS_SELECTOR, "a.preview-link")
    ARTICLE_PREVIEW_PAGE_A = (By.CSS_SELECTOR, "a.page-link")

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
    TAG_DEL_I = (By.CSS_SELECTOR, "i.ion-close-round")
    PUBLISH_BTN = (By.CSS_SELECTOR, "button")

    # 글 상세 페이지 관련 로케이터
    ARTICLE_DETAIL_TITLE_H1 = (By.TAG_NAME, "h1")
    ARTICLE_DETAIL_PROFILE_IMG = (By.CSS_SELECTOR, "div a img")
    ARTICLE_DETAIL_AUTHOR = (By.CSS_SELECTOR, "div.info > a.author")
    ARTICLE_DETAIL_DATE = (By.CSS_SELECTOR, "div.info > span.date")
    EDIT_ARTICLE_BTN = (By.CSS_SELECTOR, "span a.btn.btn-outline-secondary.btn-sm")
    DELETE_ARTICLE_BTN = (By.CSS_SELECTOR, "span button.btn.btn-outline-danger.btn-sm")
    ARTICLE_DETAIL_BODY_P = (By.CSS_SELECTOR, "div p")
    ARTICLE_COMMENT_TEXTAREA = (
        By.CSS_SELECTOR,
        'textarea[placeholder*="Write a comment..."]',
    )
    ARTICLE_POST_COMMENT_BTN = (By.CSS_SELECTOR, 'button[type*="submit"]')
    ARTICLE_COMMENT_P = (By.CSS_SELECTOR, "p.card-text")
    ARTICLE_COMMENT_AUTHOR_PROFILE_IMG = (By.CSS_SELECTOR, "a.comment-author > img")
    ARTICLE_COMMENT_AUTHOR_LINK = (By.CSS_SELECTOR, "a.comment-author:empty")
    ARTICLE_COMMENT_DEL_BTN = (By.CSS_SELECTOR, "i.ion-trash-a")

    def __init__(self, driver):
        super().__init__(driver)

    # 특정 요소의 자식 요소 찾기
    def find_child_elements(self, parents_elem: WebElement, child_locator):
        return parents_elem.find_elements(*child_locator)

    def load_article_preview_lists(self):
        # 페이지 로드 완료될 때까지 대기
        helpers = Helpers(self.driver)
        helpers.wait_until_page_load_complete()
        article_previews = self.find_elements(self.ARTICLE_PREVIEW_DIV)
        article_count = len(article_previews)
        articles = {}  # 정제된 articles 데이터를 담을 딕셔너리 변수
        if article_count == 1 and article_previews[0].text == "No articles are here... yet.":
            return article_previews[0]
        else:  # 등록 게시물이 1개 이상 존재하는 경우
            pre_authors = []
            pre_create_dates = []
            pre_favors = []
            pre_titles = []
            pre_descriptions = []
            pre_tags = []

            pre_author_elems = self.find_elements(self.ARTICLE_PREVIEW_USERNAME)
            pre_create_date_elems = self.find_elements(self.ARTICLE_PREVIEW_DATE)
            pre_favor_elems = self.find_elements(self.ARTICLE_PREVIEW_FAVOR_BTN)
            pre_title_elems = self.find_elements(self.ARTICLE_PREVIEW_TITLE_H1)
            pre_description_elems = self.find_elements(
                self.ARTICLE_PREVIEW_DESCRIPTION_P
            )
            pre_tag_elems = self.find_elements(self.TAGS_UL)

            # 게시글 작성자 텍스트 값 추출
            for author in pre_author_elems:
                author_text = author.text
                pre_authors.append(author_text)

            # 게시글 작성일 텍스트 값 추출
            for date in pre_create_date_elems:
                date_text = date.text
                pre_create_dates.append(date_text)

            # 게시글 좋아요 텍스트 값 추출
            for favor in pre_favor_elems:
                favor_text = favor.text
                pre_favors.append(favor_text)

            # 게시글 제목 텍스트 값 추출
            for title in pre_title_elems:
                title_text = title.text
                pre_titles.append(title_text)

            # 게시글 주제 텍스트 값 추출
            for description in pre_description_elems:
                # 주제 내용에 글 작성자, 날짜 정보와 read more 부분도 포함되어 필요 내용 외 삭제
                lines = description.text.split("\n")
                desc_text = lines[4]
                pre_descriptions.append(desc_text)

            # 태그 텍스트 추출
            for tag_ul in pre_tag_elems:
                current_article_tags = self.find_child_elements(tag_ul, self.TAGS_LI)
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
        # print(f"수집된 작성자 총 {len(pre_authors)}개 - : {pre_authors}\n")
        # print(f"수집된 작성일 총 {len(pre_create_dates)}개 - : {pre_create_dates}\n")
        # print(f"수집된 좋아요 수 총 {len(pre_favors)}개 - : {pre_favors}\n")
        # print(f"수집된 제목 총 {len(pre_titles)}개 - : {pre_titles}\n")
        # print(f"수집된 본문 내용 총 {len(pre_bodies)}개 - : {pre_bodies}\n")
        # print(f"수집된 태그 총 {len(pre_tags)}개 - : {pre_tags}\n")

        for i in range(len(pre_titles)):
            articles[f"article{i+1}"] = {
                "author": pre_authors[i],
                "created date": pre_create_dates[i],
                "favor count": pre_favors[i],
                "title": pre_titles[i],
                "description": pre_descriptions[i],
                "tags": pre_tags[i],
            }
        # 디버깅용
        # print(articles)
        return articles

    def click_article(self, selected_page, index):
        # 페이지 로드가 완료될 때 까지 대기
        helpers = Helpers(self.driver)
        helpers.wait_until_page_load_complete()

        # 페이지네이션이 없는 경우 (전체 게시글 갯수 10개 이하) - 0으로 파라미터 보낼 것
        if selected_page == 0:
            article_links = self.find_elements(self.ARTICLE_PREVIEW_READMORE_A)
            article_links[index - 1].click()
        else:
            pages = self.find_elements(self.ARTICLE_PREVIEW_PAGE_A)
            pages[selected_page - 1].click()
            helpers.wait_until_page_load_complete()
            article_links = self.find_elements(self.ARTICLE_PREVIEW_READMORE_A)
            article_links[index - 1].click()

    def click_preview_favorite(self, selected_page, index):
        # 페이지 로드가 완료될 때 까지 대기
        helpers = Helpers(self.driver)
        helpers.wait_until_page_load_complete()

        # 페이지네이션이 없는 경우 (전체 게시글 갯수 10개 이하) - 0으로 파라미터 보낼 것
        if selected_page == 0:
            article_links = self.find_elements(self.ARTICLE_PREVIEW_FAVOR_BTN)
            article_links[index - 1].click()
        else:
            pages = self.find_elements(self.ARTICLE_PREVIEW_FAVOR_BTN)
            pages[selected_page - 1].click()
            helpers.wait_until_page_load_complete()
            article_links = self.find_elements(self.ARTICLE_PREVIEW_FAVOR_BTN)
            article_links[index - 1].click()

    def click_preview_author_profile_img(self):
        self.click_element(self.ARTICLE_PREVIEW_PROFILE_IMG)

    def click_preview_author(self):
        self.click_element(self.ARTICLE_PREVIEW_USERNAME)

    def click_article_author_profile_img(self):
        self.click_element(self.ARTICLE_DETAIL_PROFILE_IMG)

    def click_article_author_username(self):
        self.click_element(self.ARTICLE_DETAIL_AUTHOR)

    def click_edit_article_btn(self):
        self.click_element(self.EDIT_ARTICLE_BTN)

    def click_delete_article_btn(self):
        self.click_element(self.DELETE_ARTICLE_BTN)

    def load_article_details(self):
        # 게시글 상세 내용을 담을 빈 딕셔너리 생성
        article_details = {}

        article_details["title"] = self.get_text(self.ARTICLE_DETAIL_TITLE_H1)
        article_details["author"] = self.get_text(self.ARTICLE_DETAIL_AUTHOR)
        article_details["created date"] = self.get_text(self.ARTICLE_DETAIL_DATE)
        article_details["body"] = self.get_text(self.ARTICLE_DETAIL_BODY_P)

        # 현재 게시글에 태그가 존재하는지 확인 후 조건 분기 처리
        current_article_tag_elems = self.find_child_elements(
            self.find_element(self.TAGS_UL), self.TAGS_LI
        )

        if not current_article_tag_elems:
            article_details["tags"] = ""
        else:
            if len(current_article_tag_elems) == 1:
                article_details["tags"] = current_article_tag_elems[0].text
            elif len(current_article_tag_elems) >= 2:
                # 2개 이상일 경우 태그 텍스트를 담을 빈 리스트 생성
                current_tags = []
                for tag in current_article_tag_elems:
                    current_tags.append(tag.text)
                article_details["tags"] = current_tags
        # 디버깅용
        # print(article_details)
        return article_details

    def send_comment(self, comment):
        self.send_keys(self.ARTICLE_COMMENT_TEXTAREA, comment)

    def click_post_comment_btn(self):
        self.click_element(self.ARTICLE_POST_COMMENT_BTN)

    def save_comment(self, comment):
        self.send_comment(comment)
        self.click_post_comment_btn()

    def click_delete_comment_btn(self):
        self.click_element(self.click_delete_comment_btn)

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

    def get_article_slug(self, title, userkey):
        """article 주소 방식
        - 한글은 모두 삭제
        - 공백의 경우 '-'로 대치"""
        print(title)
        # 한글 삭제
        changed_url_path = (
            "article/"
            + re.sub(r"[가-힣]+", "", title).replace(" ", "-")
            + f"-{userkey}"
        )
        if "--" in changed_url_path:
            changed_url_path = changed_url_path.replace("--", "-")
        print(changed_url_path)
        return changed_url_path

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
