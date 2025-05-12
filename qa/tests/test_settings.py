import pytest
from utils.logger import setupLogger
from pages.header.header import Header
from pages.body.home_page import HomePage
from pages.body.signin_page import SignInPage
from pages.body.settings_page import SettingsPage
from pages.body.signup_page import SignUpPage
from config.config import SETTINGS_URL
from db.db_utils import *
import time
from config.config import BASE_URL
from selenium.webdriver.remote.webdriver import WebDriver
from data.user_data import SETTING_USER_1, SETTING_USER_2, SETTING_USER_3

@pytest.mark.usefixtures("driver")
class TestSettings:
    logger = setupLogger(__qualname__)



    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, driver:WebDriver):
        driver.get(BASE_URL)
        delete_all_user()
        yield
        self.logger.info("============================")

    @pytest.mark.parametrize("user_data", [SETTING_USER_1, SETTING_USER_2, SETTING_USER_3], ids=["1", "2", "3"])
    def test_successful_update_settings(self, driver, user_data):
        """SETTING_01: 유효한 정보로 회원 정보 업데이트 성공"""
        self.logger.info("회원 정보 업데이트 테스트 시작")
        header = Header(driver)
        settingsPage = SettingsPage(driver)
        signUpPage = SignUpPage(driver)
        try:
            
            header.click_sign_up_link()
            signUpPage.sign_up()
            header.click_sign_in_link()
            header.click_settings_link()
            current_url = settingsPage.wait_until_url_and_get(SETTINGS_URL)

            assert SETTINGS_URL in current_url # 기대 결과 1
            self.logger.info("기대 결과 1 - Settings 페이지로 진입됨")

            settingsPage.change_user_info(expected_url=user_data["url"],expected_username=user_data["username"],expected_bio=user_data["bio"],expected_email=user_data["email"])

            assert all([ # 기대결과 2
            settingsPage.is_url_link_equal(user_data["url"]),
            settingsPage.is_username_equal(user_data["username"]),
            settingsPage.is_bio_equal(user_data["bio"]),
            settingsPage.is_email_equal(user_data["email"])
            ])
            self.logger.info("기대 결과 2 - 입력한 값이 입력 필드에 입력됨")
            
            settingsPage.click_update_btn()
            assert all([
                user_data["url"] in header.get_profile_img(),
                header.get_username() == user_data["username"]
            ])
            self.logger.info("기대 결과 3 - 프로필 사진과 계정명이 헤더에 노출됨")
            self.logger.info("회원 정보 입력 및 제출 완료")
        except Exception as e:
            self.logger.error(f"❌ 회원 정보 업데이트 테스트 중 오류 발생: {e}")
            assert False, "❌ 회원 정보 업데이트 테스트 중 오류 발생"
        finally:
            reset_user_info(user_data["username"]) # 테스트 종료 후 username, email 정보 초기화

    @pytest.mark.skip(reason="미구현")
    def test_successful_update_password(self,driver,password):
        """SETTING_02: 유효한 정보로 비밀번호 업데이트 성공"""
        self.logger.info("비밀번호 업데이트 테스트 시작")
        header = Header(driver)
        signinPage = SignInPage(driver)
        settingsPage = SettingsPage(driver)
        try:
            pass
        except Exception as e:
            self.logger.error(f"❌ 회원 정보 업데이트 테스트 중 오류 발생: {e}")
            assert False, "❌ 회원 정보 업데이트 테스트 중 오류 발생"