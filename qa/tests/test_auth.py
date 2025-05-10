import pytest

from config.config import BASE_URL
from data.user_data import VALID_USER 
from utils.logger import setupLogger
from pages.header.header import Header
from pages.body.home_page import HomePage
from pages.body.signup_page import SignUpPage
from pages.body.signin_page import SignInPage
from pages.body.settings_page import SettingsPage

@pytest.mark.usefixtures("driver")
class TestAuthentication:
    logger = setupLogger(__qualname__)

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, driver):
        driver.get(BASE_URL)
        yield
        self.logger.info("==================================")

    # def test_successful_signup(self, driver):
    #     """AUTH_01: 유효한 정보로 회원가입 성공"""
    #     self.logger.info("회원가입 테스트 시작")

    def test_successful_login(self, driver):
        """AUTH_02: 유효한 정보로 로그인 성공 및 사용자 정보 확인"""
        self.logger.info("유효한 정보로 로그인 테스트 시작")
        header = Header(driver)
        signInPage = SignInPage(driver)

        try:
            header.click_sign_in_link()
            signInPage.send_email_input(VALID_USER["email"])
            signInPage.send_password_input(VALID_USER["password"])
            signInPage.click_sign_in_btn()
            self.logger.info("로그인 정보 입력 및 제출 완료")

            header.wait_for_my_profile_link_appear()
            self.logger.info("사용자 정보 확인 완료")

            assert VALID_USER["username"] in header.get_username_link_text()
            self.logger.info("유효한 정보로 로그인 테스트 성공")

        except Exception as e:
            self.logger.error(f"❌ 로그인 테스트 중 오류 발생: {e}")
            assert False

    # def test_login_fail(self, driver):
    #     """AUTH_03: 잘못된 정보로 로그인 시 오류 메시지 제공 확인"""
    #     self.logger.info("맞지 않는 비밀번호로 로그인 테스트 시작")
    #     self.logger.info("미가입 이메일로 로그인 테스트 시작")

    def test_logout(self, driver):
        """AUTH_04: 로그인 상태에서 로그아웃 성공"""
        self.logger.info("로그아웃 테스트 시작")
        header = Header(driver)
        homePage = HomePage(driver)
        signInPage = SignInPage(driver)
        settingsPage = SettingsPage(driver)

        try:
            header.click_sign_in_link()
            signInPage.login()
            self.logger.info("로그인 정보 입력 및 제출 완료")

            header.click_settings_link()
            assert header.is_go_to_settings_page() # 기대 결과 1: Settings 페이지로 진입되어야 함

            settingsPage.click_logout_btn()
            assert header.is_go_to_home_page() # 기대 결과 2: 메인 화면 진입

            assert all([ # 기대 결과 3: 메인 화면에서 Your Feed 탭, New Post 링크, Settings 링크, MyProfile 링크 표시되지 않음
                homePage.is_your_feed_tab_link_disappear(),
                header.is_new_post_link_disappear(),
                header.is_settings_link_disappear(),
                header.is_my_profile_link_disappear()
            ])
            self.logger.info("로그아웃 테스트 성공")

        except Exception as e:
            self.logger.error(f"❌ 로그아웃 테스트 중 오류 발생: {e}")
            assert False