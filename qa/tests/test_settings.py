import pytest

from utils.logger import setupLogger
from pages.header.header import Header
from pages.body.home_page import HomePage
from pages.body.signin_page import SignInPage
from pages.body.settings_page import SettingsPage
from db.execute_query import *
import time

@pytest.mark.usefixtures("driver")
class TestSettings:
    logger = setupLogger(__qualname__)

    url = ["https://i.namu.wiki/i/WxfZN24op278LD9Zs0CqcmmDTf5BrsxEj-jKSFSKGshojImAMcxAQET1l6DX5pmCKffUsSm65A1T0yUg0RVILEiobkjl4EHQvprjO7BOl7zzUZv6NjFkt8G1j7O1n98hvxqYx6pUyCLFiSR3hLbwRg.webp","https://item.kakaocdn.net/do/eca065fa2b45d3cc588798b70ee7ec2ff43ad912ad8dd55b04db6a64cddaf76d","Wrong_URL"]
    username = ["1", "2", "3"]
    bio = ["Sample bio 1", "Sample bio 2", "Sample bio 3"]
    email = ["1@1.1", "2@2.2", "3@3.3"]
    password = ["1", "2", "3"]
    test_data = list(zip(url, username, bio, email, password))

    @pytest.fixture(autouse=True)
    def teardown(self):
        yield
        self.logger.info("============================")

    @pytest.mark.parametrize("url, username, bio, email", [data[:4] for data in test_data], ids=[i+1 for i in range(len(test_data))])
    def test_successful_update_settings(self, driver, url, username, bio, email):
        """SETTING_01: 유효한 정보로 회원 정보 업데이트 성공"""
        self.logger.info("회원 정보 업데이트 테스트 시작")
        header = Header(driver)
        loginPage = SignInPage(driver)
        settingsPage = SettingsPage(driver)

        header.click_sign_in_link()
        loginPage.login()
        header.click_settings_link()
        current_url = settingsPage.current_url()
        settingsPage.send_url_link_input(url)
        settingsPage.send_username_input(username)
        settingsPage.send_bio_input(bio)
        settingsPage.send_email_input(email)
        
        assert "/settings" in current_url  , "URL이 일치하지 않음"
        self.logger.info("Settings 페이지 진입 확인")
        url_link_input_value = settingsPage.get_attribute(settingsPage.URL_LINK_INPUT, "value")
        username_input_value = settingsPage.get_attribute(settingsPage.USERNAME_INPUT, "value")
        bio_input_value = settingsPage.get_attribute(settingsPage.BIO_INPUT, "value")
        email_input_value = settingsPage.get_attribute(settingsPage.EMAIL_INPUT, "value")
        assert url == url_link_input_value, "URL 링크 입력값이 일치하지 않음"
        assert username == username_input_value, "사용자 이름 입력값이 일치하지 않음"
        assert bio == bio_input_value, "바이오 입력값이 일치하지 않음"
        assert email == email_input_value, "이메일 입력값이 일치하지 않음"


        self.logger.info("회원 정보 입력 및 제출 완료")