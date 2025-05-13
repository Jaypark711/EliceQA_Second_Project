import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from config.config import BASE_URL
from data.user_data import  VALID_USER
from pages.header.header import Header
from pages.body.home_page import HomePage
from pages.body.signup_page import SignUpPage
from pages.body.article_page import ArticlePage
from pages.body.profile_page import ProfilePage
from utils.logger import setupLogger
from db.db_utils import init_db, run_prisma_seed, get_favorited_article_title_by_username

@pytest.mark.usefixtures("driver")
class TestSocial:
    logger = setupLogger(__qualname__)

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, driver:WebDriver):
        init_db() # 테스트 환경 초기화: 상태 의존성을 제거하고 동일한 초기 조건 보장
        run_prisma_seed() # 초기 데이터 생성
        driver.get(BASE_URL)

        yield

        self.logger.info("============================")
    
    def test_article_favorite_function(self,driver):
        """SOCIAL_01: 유효한 정보로 비밀번호 업데이트 성공"""
        self.logger.info("즐겨찾기 기능 테스트 시작")
        header = Header(driver)
        signupPage = SignUpPage(driver)
        homePage = HomePage(driver)
        articlePage = ArticlePage(driver)
        
        try:
            # 테스트 환경 세팅
            header.click_sign_up_link()
            signupPage.sign_up()

            # 테스트 시나리오 시작
            homePage.click_global_feed_tab_link()
            articlePage.click_preview_favorite(0, 1)

            first_article = articlePage.load_first_article_data()
            assert first_article['favor count'] == '1' # 기대 결과 1 : 좋아요가 하나 증가한 채로 노출됨
            self.logger.info("기대 결과 1 : 좋아요가 하나 증가한 채로 노출됨")
            
            assert get_favorited_article_title_by_username(VALID_USER["username"]) == first_article['title'] # 기대 결과 2 : db에 좋아요 누른 게시글이 노출됨
            self.logger.info("기대 결과 2 : db에 좋아요 누른 게시글이 노출됨")
            
        except Exception as e:
            self.logger.error(f"❌ SOCIAL_01 테스트 중 오류 발생: {e}")
            assert False, "❌ SOCIAL_01 테스트 중 오류 발생"

    def test_author_follow_function(self,driver):
        """SOCIAL_02: 다른 사용자 팔로우 및 언팔로우 기능 확인"""
        self.logger.info("팔로우 및 언팔로우 기능 테스트 시작")
        header = Header(driver)
        homePage = HomePage(driver)
        signupPage = SignUpPage(driver)
        articlePage = ArticlePage(driver)
        profilePage = ProfilePage(driver)

        try:
            # 테스트 환경 세팅
            header.click_sign_up_link()
            signupPage.sign_up()

            # 테스트 시나리오 시작
            homePage.click_global_feed_tab_link()
            articlePage.click_preview_author()
            followed_user = profilePage.get_username_title_text()
            profilePage.click_follow_btn()

            header.click_home_link()
            homePage.click_your_feed_tab_link()
            article_authors = [ article_info['author'] for article_info in articlePage.load_article_preview_lists().values() ]
            assert set(article_authors) == {followed_user} # 기대 결과 1 : article 리스트의 author이 follow한 author과 전부 일치
            self.logger.info("기대 결과 1 : article 리스트의 author이 follow한 author과 전부 일치")

            articlePage.click_preview_author()
            profilePage.click_unfollow_btn()

            header.click_home_link()
            homePage.click_your_feed_tab_link()
            assert articlePage.is_empty_text_div_show() # 기대 결과 2 : 팔로우한 author이 없을 때 No articles here이 노출됨
            self.logger.info("기대 결과 2 : 팔로우한 author이 없을 때 No articles here이 노출됨")

        except Exception as e:
            self.logger.error(f"❌ SOCIAL_02 테스트 중 오류 발생: {e}")
            assert False, "❌ SOCIAL_02 테스트 중 오류 발생"
