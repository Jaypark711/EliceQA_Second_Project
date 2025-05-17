import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from config.config import BASE_URL
from data.user_data import VALID_USER
from data.dummy_data import COMMENT_DATA_1
from pages.home_page import HomePage
from pages.sign_up_page import SignUpPage
from db.db_utils import init_db, run_prisma_seed
from utils.logger import setupLogger

@allure.suite("test_comment.py")
@allure.sub_suite("COMMENT TEST")
@pytest.mark.usefixtures("driver")
class TestCommentPage:
    logger = setupLogger(__qualname__)

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, driver: WebDriver):
        init_db() # 테스트 환경 초기화
        run_prisma_seed() # 초기 데이터 생성
        driver.get(BASE_URL)

        yield

        self.logger.info("=================================================================")

    @allure.title("[CMT_01]: 댓글 - 게시 및 삭제")
    @allure.description("특정 게시글에 댓글 작성 및 삭제 확인")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("comment", [COMMENT_DATA_1])
    def test_successful_comment(self, driver, comment):
        self.logger.info("▶️ 댓글 등록 후 삭제 테스트 시작")
        
        homePage = HomePage(driver)
        signupPage = SignUpPage(driver)

        try:
            # 테스트 환경 세팅
            homePage.header.click_sign_up_link()
            signupPage.sign_up.sign_up()

            # 테스트 시나리오 시작
            homePage.tabs.click_global_feed_tab_link()
            first_article = homePage.article.load_first_article_data()
            homePage.article.click_article(0,1)
            detail_article = homePage.article.load_article_details()
            assert all([ 
                first_article["title"] == detail_article["title"], 
                first_article["author"] == detail_article["author"],
                first_article["created date"] == detail_article["created date"]
            ])
            self.logger.info("✅ 기대 결과 1 : 누른 게시글로 이동되어 노출됨")

            homePage.article.send_comment(comment)
            assert homePage.article.get_text_from_comment_textarea() == comment
            self.logger.info("✅ 기대 결과 2 : 입력한 값이 댓글 입력 필드에 반영됨")

            homePage.article.click_post_comment_btn()
            assert all([
                homePage.article.get_text_from_comment() == comment, 
                homePage.article.get_text_from_author() == VALID_USER["username"] 
            ])
            self.logger.info("✅ 기대 결과 3 : 입력한 값이 댓글로 정상 등록됨")

            homePage.article.click_delete_comment_btn()
            assert all([
                homePage.article.is_comment_disappear(),
                homePage.article.is_author_link_disappear()
            ])
            self.logger.info("✅ 기대 결과 4 : 댓글 삭제 확인")
            self.logger.info("🎉 댓글 등록 후 삭제 테스트 완료")
        except Exception as e:
            self.logger.error(f"❌ CMT_01 테스트 중 오류 발생: {e}")
            assert False, "❌ CMT_01 테스트 중 오류 발생"