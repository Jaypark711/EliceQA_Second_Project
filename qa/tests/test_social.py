import pytest
from utils.logger import setupLogger
from pages.header.header import Header
from pages.body.home_page import HomePage
from pages.body.signin_page import SignInPage
from pages.body.settings_page import SettingsPage
from pages.body.signup_page import SignUpPage
from pages.body.article_page import ArticlePage
from pages.body.profile_page import ProfilePage
from config.config import SETTINGS_URL
from data.user_data import  VALID_USER
from db.db_utils import *
import time
from config.config import BASE_URL
from selenium.webdriver.remote.webdriver import WebDriver

@pytest.mark.usefixtures("driver")
class TestSocial:
    logger = setupLogger(__qualname__)

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, driver:WebDriver):
        init_db()
        run_prisma_seed()
        driver.get(BASE_URL)
        yield
        self.logger.info("============================")
    
    def test_article_favorite_function(self,driver):
        """SOCIAL_01: 유효한 정보로 비밀번호 업데이트 성공"""
        header = Header(driver)
        signupPage = SignUpPage(driver)
        homePage = HomePage(driver)
        articlePage = ArticlePage(driver)
        self.logger.info("즐겨찾기 기능 테스트 시작")
        try:
            header.click_sign_up_link()
            signupPage.sign_up()
            homePage.click_global_feed_tab_link()
            articlePage.click_preview_favorite(0,1)
            articles = articlePage.load_article_preview_lists()
            first_article = list(articles.values())[0]
            assert first_article['favor count'] == '1' # 기대 결과 1 : 좋아요가 하나 증가한 채로 노출됨
            self.logger.info("기대 결과 1 : 좋아요가 하나 증가한 채로 노출됨")
            
            assert get_title_where_favorite(VALID_USER["username"]) == first_article['title'] # 기대 결과 2 : db에 좋아요 누른 게시글이 노출됨
            self.logger.info("기대 결과 2 : db에 좋아요 누른 게시글이 노출됨")
        except Exception as e:
            self.logger.error(f"❌ SOCIAL_01 테스트 중 오류 발생: {e}")
            assert False, "❌ SOCIAL_01 테스트 중 오류 발생"

    def test_author_follow_function(self,driver):
        try:
            header = Header(driver)
            signupPage = SignUpPage(driver)
            homePage = HomePage(driver)
            articlePage = ArticlePage(driver)
            profilePage = ProfilePage(driver)
            header.click_sign_up_link()
            signupPage.sign_up()
            homePage.click_global_feed_tab_link()
            articlePage.click_preview_author()
            followed_user = profilePage.get_name_from_follow_btn()
            profilePage.click_follow_btn()
            header.click_home_link()
            article_list = [ info['author'] for info in articlePage.load_article_preview_lists().values() ]
            
            assert set(article_list) == {followed_user} # 기대 결과 1 : article 리스트의 author이 follow한 author과 전부 일치
            self.logger.info("기대 결과 1 : article 리스트의 author이 follow한 author과 전부 일치")

            articlePage.click_preview_author()
            profilePage.click_unfollow_btn()
            header.click_home_link()
            assert articlePage.is_empty_text_div_show() # 기대 결과 2 : 팔로우한 author이 없을 때 No articles here이 노출됨
            self.logger.info("기대 결과 2 : 팔로우한 author이 없을 때 No articles here이 노출됨")

        except Exception as e:
            self.logger.error(f"❌ SOCIAL_02 테스트 중 오류 발생: {e}")
            assert False, "❌ SOCIAL_02 테스트 중 오류 발생"
