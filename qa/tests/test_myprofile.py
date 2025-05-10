import pytest

from pages.header.header import Header
from pages.body.signin_page import SignInPage
from pages.body.profile_page import ProfilePage
from utils.logger import setupLogger

@pytest.mark.usefixtures("driver")
class TestMyProfile:
    logger = setupLogger(__qualname__)

    @pytest.fixture(autouse=True)
    def teardown(self):
        yield
        self.logger.info("==================================")

    # def test_show_my_articles(self, driver):
    #     """MYPROFILE_01: 마이프로필에서 내가 작성한 게시글 목록(My Articles) 표시 확인"""
    #     self.logger.info("마이프로필에서 My Articles 탭 테스트 시작")
    #     header = Header(driver)
    #     signInPage = SignInPage(driver)
    #     profilePage = ProfilePage(driver)

    #     header.click_sign_in_link()
    #     signInPage.login()
    #     self.logger.info("로그인 성공")

    #     header.click_my_profile_link()
    #     profilePage.click_my_article_tab_link()
    #     assert profilePage.is_my_article_tab_active() == True
    #     self.logger.info("마이 프로필에서 My Articles 탭 클릭 및 탭 활성화 확인")

    #     # TODO: 내가 작성한 게시글만 보이는지 확인 (게시글 정보 불러오는 함수 구현 전까지 대기)

    # def test_show_favorited_articles(self, driver):
    #     """MYPROFILE_02: 마이프로필에서 좋아요 누른 게시글 목록(Favorited Articles) 표시 확인"""
    #     self.logger.info("마이프로필에서 Favorited Articles 탭 테스트 시작")
    #     header = Header(driver)
    #     signInPage = SignInPage(driver)
    #     profilePage = ProfilePage(driver)

    #     header.click_sign_in_link()
    #     signInPage.login()
    #     self.logger.info("로그인 성공")

    #     header.click_my_profile_link()
    #     profilePage.click_favorited_article_tab_link()
    #     assert profilePage.is_favorited_article_tab_active() == True
    #     self.logger.info("마이 프로필에서 Favorited Articles 탭 클릭 및 탭 활성화 확인")

    #     # TODO: 내가 즐겨찾기한 게시글만 보이는지 확인 (게시글 정보 불러오는 함수 구현 전까지 대기)

    def test_go_to_settings_from_profile(self, driver):
        """MYPROFILE_03: 마이프로필에서 '프로필 수정(Edit Profile Settings)' 버튼 클릭 시 설정 페이지로 이동 확인"""
        self.logger.info("마이 프로필에서 Edit Profile Settings 버튼 테스트 시작")
        header = Header(driver)
        signInPage = SignInPage(driver)
        profilePage = ProfilePage(driver)

        header.click_sign_in_link()
        signInPage.login()
        self.logger.info("로그인 성공")

        profilePage.click_edit_profile_settings_btn()
        self.logger.info("Edit Profile Settings 버튼 클릭 완료")

        assert profilePage.is_go_to_settings_page() == True
        self.logger.info("설정 페이지 이동 확인 완료")