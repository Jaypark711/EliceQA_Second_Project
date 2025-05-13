import pytest
from db.db_utils import *
from config.config import BASE_URL
from utils.logger import setupLogger
from pages.header.header import Header
from pages.body.home_page import HomePage
from pages.body.signin_page import SignInPage
from pages.body.article_page import ArticlePage
from pages.body.signup_page import SignUpPage
from selenium.webdriver.remote.webdriver import WebDriver
from data.user_data import VALID_USER
import time


@pytest.mark.usefixtures("driver")
class TestAriclePage:
    logger = setupLogger(__qualname__)

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, driver: WebDriver):
        init_db() # 테스트 환경 초기화
        driver.get(BASE_URL)

        yield

        self.logger.info("==================================")

    def test_successful_comment(self,driver):
        """CMT_01 : 코멘트 등록 후 삭제 테스트"""
        header = Header(driver)
        signupPage = SignUpPage(driver)
        homePage = HomePage(driver)
        articlePage = ArticlePage(driver)
        try:
            self.logger.info("댓글 등록 후 삭제 테스트 시작")
            run_prisma_seed()
            header.click_sign_up_link()
            signupPage.sign_up()
            homePage.click_global_feed_tab_link()
            first_article = articlePage.load_first_article_data()
            articlePage.click_article(0,1)
            detail_article = articlePage.load_article_details()
            assert all([ # 기대 결과 1 : 누른 게시글로 이동되어 노출됨
                first_article["title"] == detail_article["title"],
                first_article["author"] == detail_article["author"],
                first_article["created date"] == detail_article["created date"]
                ])
            self.logger.info("기대 결과 1 : 누른 게시글로 이동되어 노출됨")
            # TODO: 하드코딩 fix 필요
            hardcoding_data = "임의의 하드코딩된 테스트 데이터"
            articlePage.send_comment(hardcoding_data)
            assert articlePage.get_text_from_comment_textarea() == hardcoding_data # 기대 결과 2 : 입력한 값이 댓글 입력 필드에 반영됨
            self.logger.info("기대 결과 2 : 입력한 값이 댓글 입력 필드에 반영됨")
            articlePage.click_post_comment_btn()
            assert all([ # 기대 결과 3 : 입력한 값이 댓글로 정상 등록됨
            articlePage.get_text_from_comment() == hardcoding_data, 
            articlePage.get_text_from_author() == VALID_USER["username"] 
            ])
            self.logger.info("기대 결과 3 : 입력한 값이 댓글로 정상 등록됨")

            articlePage.click_comment_del_btn()
            assert all([ # 기대 결과 4 : 댓글 삭제 확인
                articlePage.is_comment_disappear(),
                articlePage.is_author_link_disappear()
            ])
            self.logger.info("기대 결과 4 : 댓글 삭제 확인")
            self.logger.info("댓글 등록 후 삭제 테스트 완료")
        except Exception as e:
            self.logger.error(f"❌ CMT_01 테스트 중 오류 발생: {e}")
            assert False, "❌ CMT_01 테스트 중 오류 발생"
