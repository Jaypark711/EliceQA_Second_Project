import pytest
import allure
from db.db_utils import *
from config.config import BASE_URL
from data.user_data import VALID_USER
from utils.logger import setupLogger
from utils.helpers import Helpers
from pages.header.header import Header
from pages.body.home_page import HomePage
from pages.body.signin_page import SignInPage
from pages.body.signup_page import SignUpPage
from pages.body.article_page import ArticlePage
from pages.body.editor_page import EditorPage
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
import time

@allure.suite("test_article.py")
@pytest.mark.usefixtures("driver")
@allure.sub_suite("ARTICLE TEST")
class TestAriclePage:
    logger = setupLogger(__qualname__)

    input_article_title = f"{VALID_USER["username"]}_작성 테스트"
    input_article_desc = "테스트 주제"
    input_article_body = "테스트 게시글 본문입니다."
    input_article_tags = ["태그1", "태그2"]

    modi_article_title = f"{VALID_USER["username"]}_수정 테스트"
    modi_article_desc = "테스트 수정"
    modi_article_body = "테스트 게시글 수정한 본문입니다."
    modi_article_tags = ["추가 태그1", "추가 태그2"]

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, driver: WebDriver):
        init_db()  # 테스트 환경 초기화
        driver.get(BASE_URL)

        yield

        self.logger.info("==================================")

    # @pytest.mark.skip(reason="Passed")
    @allure.title("[ARTICLE_01]: 게시글 - 신규 등록")
    @allure.description("로그인 후 새 게시글 작성 및 게시 성공 확인 (제목, 본문, 태그 포함)") 
    def test_save_new_article(self, driver: WebDriver):
        signupPage = SignUpPage(driver)
        header = Header(driver)
        articlePage = ArticlePage(driver)
        editorPage = EditorPage(driver)

        try:
            header.click_sign_up_link()
            signupPage.sign_up()

            header.click_new_post_link()
            editorPage.save_article(
                self.input_article_title,
                self.input_article_desc,
                self.input_article_body,
                self.input_article_tags,
            )
            saved_article = articlePage.load_article_details()

            # 비교용 slug 생성을 위해 DB에서 유저 키 값 받아오기
            user_id = get_user_id_by_username(VALID_USER["username"])
            new_slug = articlePage.get_article_slug(self.input_article_title, user_id)

            # 현재 url과 제목 값 기반으로 만들어진 url과 비교
            assert driver.current_url == BASE_URL + new_slug
            self.logger.info("✅ 현재 URL이 제목 값에 따라 정상 생성되었습니다. ")

            # 저장된 제목과 실제 입력한 제목 비교
            assert saved_article["title"] == self.input_article_title
            self.logger.info(
                "✅ 신규 게시글 제목이 입력한 값으로 정상 저장되었습니다. "
            )

            # 저장된 본문 내용과 실제 입력한 본문 내용 비교
            assert saved_article["body"] == self.input_article_body
            self.logger.info(
                "✅ 신규 게시글 본문 내용이 입력한 값으로 정상 저장되었습니다. "
            )

            # 저장된 태그들 값과 실제 입력한 태그들 값 비교
            assert saved_article["tags"] == self.input_article_tags
            self.logger.info(
                "✅ 신규 게시글 태그가 입력한 값으로 정상 저장되었습니다. "
            )

            # 게시글이 DB에 정말로 저장되었는지 확인 (By. title)
            assert get_articles_by_title(saved_article["title"]) != None
            self.logger.info(
                "✅ 신규 게시글 제목으로 DB 조회 시 해당 글이 정상적으로 조회되었습니다. "
            )

        except Exception as e:
            self.logger.error(f"❌ ARTICLE_01 테스트 중 오류 발생: {e}")
            assert False, "❌ ARTICLE_01 테스트 중 오류 발생"

    # @pytest.mark.skip(reason="Passed")
    @allure.title("[ARTICLE_02]: 게시글 - 조회")
    @allure.description("게시글 목록(Global Feed) 게시글 표시 확인") 

    def test_load_article_previews(self, driver: WebDriver):
        signupPage = SignUpPage(driver)
        header = Header(driver)
        homePage = HomePage(driver)
        articlePage = ArticlePage(driver)
        editorPage = EditorPage(driver)
        helpers = Helpers(driver)

        try:
            header.click_sign_up_link()
            signupPage.sign_up()

            homePage.click_global_feed_tab_link()
            helpers.wait_until_page_load_complete()
            article_preview_lists = articlePage.load_article_preview_lists()

            # 게시글 목록이 없을 경우
            if type(article_preview_lists) == WebElement:
                assert articlePage.is_empty_text_div_show()
                self.logger.info("✅ 게시글 없을 시 Empty 문구 정상 제공 확인")

            # Empty 문구 확인 후 신규 글 작성
            header.click_new_post_link()

            editorPage.save_article(
                self.input_article_title,
                self.input_article_desc,
                self.input_article_body,
                self.input_article_tags,
            )

            header.click_home_link()
            homePage.click_global_feed_tab_link()

            helpers.wait_until_page_load_complete()
            article_preview_lists = articlePage.load_article_preview_lists()

            # 게시글이 존재한다면 DB 저장 여부를 확인할 타이틀 값만 추출
            if len(article_preview_lists) != 0:
                preview_titles = []
                for preview in article_preview_lists.values():
                    if isinstance(preview, dict) and "title" in preview:
                        preview_titles.append(preview["title"])
                # print(preview_titles)

            # 게시글 목록이 있을 경우 - 실제 DB에 등록된 게시글인지 확인
            for title in preview_titles:
                assert get_articles_by_title(title) != None
                self.logger.info(
                    "✅ 게시글 있을 시 DB에서 정상적으로 게시글 목록 로드 확인"
                )

        except Exception as e:
            self.logger.error(f"❌ ARTICLE_02 테스트 중 오류 발생: {e}")
            assert False, "❌ ARTICLE_02 테스트 중 오류 발생"

    # @pytest.mark.skip(reason="Passed")
    @allure.title("[ARTICLE_03]: 게시글 - 상세 페이지")
    @allure.description("특정 게시글 상세 페이지 접근 및 내용(제목, 본문) 확인") 
    def test_confirm_article_detail(self, driver: WebDriver):
        signupPage = SignUpPage(driver)
        header = Header(driver)
        homePage = HomePage(driver)
        articlePage = ArticlePage(driver)
        editorPage = EditorPage(driver)
        try:
            header.click_sign_up_link()
            signupPage.sign_up()

            header.click_new_post_link()
            editorPage.save_article(
                self.input_article_title,
                self.input_article_desc,
                self.input_article_body,
                self.input_article_tags,
            )

            header.click_home_link()

            # 다른 계정 글 확인용 dummy 데이터 삽입하기
            run_prisma_seed()

            # 다른 계정이 쓴 글 진입 (dummy)
            homePage.click_global_feed_tab_link()
            articlePage.click_article(0, 1)
            others_slug = driver.current_url.replace(f"{BASE_URL}article/", "")
            others_article = articlePage.load_article_details()

            others_db_article_datas = get_article_details_by_slug(others_slug)
            assert others_db_article_datas[2] == others_article["title"]
            self.logger.info("✅ 글 제목 내용 확인")

            assert others_db_article_datas[4] == others_article["body"]
            self.logger.info("✅ 글 본문 내용 확인")

            assert articlePage.is_not_my_article() == True
            self.logger.info("✅ 다른 계정이 쓴 글 수정 및 삭제 불가함을 확인했습니다.")

            # 현재 유저가 쓴 글 진입
            header.click_home_link()
            homePage.click_global_feed_tab_link()
            articlePage.click_article(0, len(articlePage.load_article_preview_lists()))

            my_slug = driver.current_url.replace(f"{BASE_URL}article/", "")
            my_article = articlePage.load_article_details()

            my_db_article_datas = get_article_details_by_slug(my_slug)

            assert my_db_article_datas[2] == my_article["title"]
            self.logger.info("✅ 글 제목 내용 확인")

            assert my_db_article_datas[4] == my_article["body"]
            self.logger.info("✅ 글 본문 내용 확인")

            assert articlePage.is_my_article() == True
            self.logger.info("✅ 내 계정이 쓴 글 수정 및 삭제 가능함을 확인했습니다.")

        except Exception as e:
            self.logger.error(f"❌ ARTICLE_03 테스트 중 오류 발생: {e}")
            assert False, "❌ ARTICLE_03 테스트 중 오류 발생"

    # @pytest.mark.skip(reason="Passed")
    @allure.title("[ARTICLE_04]: 게시글 - 수정")
    @allure.description("자신이 작성한 게시글 수정 성공 확인") 

    def test_modi_my_article(self, driver):
        signupPage = SignUpPage(driver)
        header = Header(driver)
        articlePage = ArticlePage(driver)
        editorPage = EditorPage(driver)
        header.click_sign_up_link()
        signupPage.sign_up()

        # 신규 글 작성
        header.click_new_post_link()
        editorPage.save_article(
            self.input_article_title,
            self.input_article_desc,
            self.input_article_body,
            self.input_article_tags,
        )

        # 글 상세 화면에서 수정 버튼 선택
        articlePage.click_edit_article_btn()

        # 수정 화면에서 글 내용 변경 후 저장
        editorPage.delete_selected_tags((self.input_article_tags[0],))
        editorPage.save_article(
            self.modi_article_title,
            self.modi_article_desc,
            self.modi_article_body,
            self.modi_article_tags,
        )

        # *글 상세 화면에서 변경 내용 확인
        modified_article = articlePage.load_article_details()

        # 변경될 slug 확인을 위해 user_id 추출
        user_id = get_user_id_by_username(VALID_USER["username"])
        new_slug = articlePage.get_article_slug(self.modi_article_title, user_id)

        # 현재 url과 제목 값 기반으로 만들어진 url과 비교
        assert driver.current_url == BASE_URL + new_slug
        self.logger.info("✅ 현재 URL이 수정된 제목 값에 따라 정상 변경 되었습니다. ")

        # 저장된 제목과 실제 입력한 제목 비교
        assert modified_article["title"] == self.modi_article_title
        self.logger.info("✅ 게시글 제목이 수정한 입력한 값으로 정상 저장되었습니다. ")

        # 저장된 본문 내용과 실제 입력한 본문 내용 비교
        assert modified_article["body"] == self.modi_article_body
        self.logger.info("✅ 게시글 본문 내용이 수정한 값으로 정상 저장되었습니다. ")

        # 저장된 태그들 값과 실제 입력한 태그들 값 비교
        self.modi_article_tags.insert(
            0, self.input_article_tags[1]
        )  # 삭제하지 않은 태그 값 비교를 위해 리스트에 추가
        assert modified_article["tags"] == self.modi_article_tags
        self.logger.info("✅ 게시글 태그가 수정한 값으로 정상 저장되었습니다. ")

        # 게시글이 DB에 정말로 저장되었는지 확인 (By. title)
        assert get_articles_by_title(modified_article["title"]) != None
        self.logger.info(
            "✅ 변경된 게시글 제목으로 DB 조회 시 해당 글이 정상적으로 조회되었습니다. "
        )

    # @pytest.mark.skip(reason="Passed")
    @allure.title("[ARTICLE_05]: 게시글 - 삭제")
    @allure.description("자신이 작성한 게시글 삭제 성공 확인") 

    def test_del_my_article(self, driver):
        signupPage = SignUpPage(driver)
        header = Header(driver)
        articlePage = ArticlePage(driver)
        editorPage = EditorPage(driver)

        header.click_sign_up_link()
        signupPage.sign_up()

        header.click_new_post_link()
        editorPage.save_article(
            self.input_article_title,
            self.input_article_desc,
            self.input_article_body,
            self.input_article_tags,
        )
        saved_article = articlePage.load_article_details()

        articlePage.click_delete_article_btn()

        # DB에서 글 삭제 되었는지 확인하기
        assert get_articles_by_title(saved_article["title"]) == None
        self.logger.info(
            "✅ 삭제한 게시글 제목으로 DB 조회 시 해당 글이 정상적으로 삭제되었습니다. "
        )
