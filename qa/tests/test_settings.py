import time
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from config.config import BASE_URL
from data.user_data import VALID_USER, SETTING_USER_1, SETTING_USER_2, SETTING_USER_3
from pages.header.header import Header
from pages.body.home_page import HomePage
from pages.body.signin_page import SignInPage
from pages.body.signup_page import SignUpPage
from pages.body.settings_page import SettingsPage
from utils.logger import setupLogger
from db.db_utils import init_db

@pytest.mark.usefixtures("driver")
class TestSettings:
    logger = setupLogger(__qualname__)

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, driver:WebDriver):
        init_db() # 테스트 환경 초기화: 상태 의존성을 제거하고 동일한 초기 조건 보장
        driver.get(BASE_URL)

        yield

        self.logger.info("============================")

    @pytest.mark.parametrize("user_data", [SETTING_USER_1, SETTING_USER_2, SETTING_USER_3])
    def test_successful_update_settings(self, driver, user_data):
        """SETTING_01: 유효한 정보로 회원 정보 업데이트 성공"""
        self.logger.info("회원 정보 업데이트 테스트 시작")
        header = Header(driver)
        settingsPage = SettingsPage(driver)
        signUpPage = SignUpPage(driver)

        try:
            # 테스트 환경 세팅
            header.click_sign_up_link()
            signUpPage.sign_up()

            # 테스트 시나리오 시작
            header.click_settings_link()
            assert header.is_go_to_settings_page() # 기대 결과 1: Settings 페이지로 진입되어야 함
            self.logger.info("기대 결과 1 - Settings 페이지로 진입됨")

            settingsPage.change_user_info(url = user_data["url"], username = user_data["username"], bio = user_data["bio"], email = user_data["email"])
            assert all([ # 기대 결과 2: 입력한 값이 입력 필드에 입력되어야 함
                settingsPage.get_url_link_input_value() == user_data["url"],
                settingsPage.get_username_input_value() == user_data["username"],
                settingsPage.get_bio_input_value() == user_data["bio"],
                settingsPage.get_email_input_value() == user_data["email"]
            ])
            self.logger.info("기대 결과 2 - 입력한 값이 입력 필드에 입력됨")
            
            settingsPage.click_update_btn()
            assert all([ # 기대 결과 3: 업데이트 후 Header - [마이프로필] 영역에 {이미지 링크}와 {사용자명}이 노출되어야 함
                user_data["url"] in header.get_profile_img(),
                user_data["username"] == header.get_username()
            ])
            self.logger.info("기대 결과 3 - 프로필 사진과 계정명이 헤더에 노출됨")
            self.logger.info("회원 정보 입력 및 제출 완료")

        except Exception as e:
            self.logger.error(f"❌ SETTING_01 테스트 중 오류 발생: {e}")
            assert False

    @pytest.mark.parametrize("user_data", [SETTING_USER_1, SETTING_USER_2, SETTING_USER_3])
    def test_successful_update_password(self,driver,user_data):
        """SETTING_02: 유효한 정보로 비밀번호 업데이트 성공"""
        self.logger.info("비밀번호 업데이트 테스트 시작")
        header = Header(driver)
        signinPage = SignInPage(driver)
        signupPage = SignUpPage(driver)
        settingsPage = SettingsPage(driver)
        homePage = HomePage(driver)
        
        try:
            # 테스트 환경 세팅
            header.click_sign_up_link()
            signupPage.sign_up()

            # 테스트 시나리오 시작
            header.click_settings_link()
            assert header.is_go_to_settings_page() # 기대 결과 1: Settings 페이지로 진입되어야 함
            self.logger.info("기대 결과 1 - Settings 페이지로 진입됨")

            settingsPage.change_user_info(password=user_data["password"])
            assert settingsPage.get_password_input_value() == user_data["password"] # 기대 결과 2: 입력한 값이 입력 필드에 입력되어야 함
            self.logger.info("기대 결과 2 - 입력한 값이 입력 필드에 입력됨")

            settingsPage.click_update_btn()
            self.logger.info("비밀번호 업데이트 성공")

            time.sleep(1) # TODO: time.sleep(1) 외에 해결책 찾지 못함
            header.click_settings_link()
            self.logger.info("세팅 링크 클릭")

            settingsPage.click_logout_btn()
            self.logger.info("로그아웃 성공")

            header.click_sign_in_link()
            signinPage.send_email_input(VALID_USER["email"])
            signinPage.send_password_input(user_data["password"])
            signinPage.click_sign_in_btn()

            assert all([ # 기대 결과 5: 메인 화면에 Your Feed 탭, New Post 링크, Settings 링크, MyProfile 링크 추가 표시
                homePage.is_your_feed_tab_link_appear(),
                header.is_new_post_link_appear(),
                header.is_settings_link_appear(),
                header.is_my_profile_link_appear()
            ])
            self.logger.info("변경된 비밀번호로 로그인 됨 확인")
            self.logger.info("비밀번호 업데이트 테스트 완료")

        except Exception as e:
            self.logger.error(f"❌ SETTING_02 테스트 중 오류 발생: {e}")
            assert False