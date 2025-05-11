import pytest
from utils.logger import setupLogger
from pages.header.header import Header
from pages.body.home_page import HomePage
from pages.body.signin_page import SignInPage
from pages.body.settings_page import SettingsPage
from config.config import SETTINGS_URL
from db.execute_query import *
import time
from config.config import BASE_URL
from selenium.webdriver.remote.webdriver import WebDriver

@pytest.mark.usefixtures("driver")
class TestSettings:
    logger = setupLogger(__qualname__)

    url = ["https://i.namu.wiki/i/WxfZN24op278LD9Zs0CqcmmDTf5BrsxEj-jKSFSKGshojImAMcxAQET1l6DX5pmCKffUsSm65A1T0yUg0RVILEiobkjl4EHQvprjO7BOl7zzUZv6NjFkt8G1j7O1n98hvxqYx6pUyCLFiSR3hLbwRg.webp","https://item.kakaocdn.net/do/eca065fa2b45d3cc588798b70ee7ec2ff43ad912ad8dd55b04db6a64cddaf76d","Wrong_URL"]
    username = ["user1", "user2", "user3"]
    bio = ["Sample bio 1", "Sample bio 2", "Sample bio 3"]
    email = ["1@1.1", "2@2.2", "3@3.3"]
    password = ["1", "2", "3"]
    test_data = list(zip(url, username, bio, email, password))

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, driver:WebDriver):
        driver.get(BASE_URL)
        yield
        self.logger.info("============================")

    @pytest.mark.parametrize("url, username, bio, email", [data[:4] for data in test_data], ids=[i+1 for i in range(len(test_data))])
    def test_successful_update_settings(self, driver, url, username, bio, email):
        """SETTING_01: 유효한 정보로 회원 정보 업데이트 성공"""
        self.logger.info("회원 정보 업데이트 테스트 시작")
        header = Header(driver)
        loginPage = SignInPage(driver)
        settingsPage = SettingsPage(driver)
        try:
            header.click_sign_in_link()
            loginPage.login()
            header.click_settings_link()
            current_url = settingsPage.wait_until_url_and_get(SETTINGS_URL)

            assert SETTINGS_URL in current_url # 기대 결과 1
            self.logger.info("기대 결과 1 - Settings 페이지로 진입됨")

            settingsPage.send_url_link_input(url)
            settingsPage.send_username_input(username)
            settingsPage.send_bio_input(bio)
            settingsPage.send_email_input(email)

            assert all([ # 기대결과 2
            settingsPage.is_url_link_equal(url),
            settingsPage.is_username_equal(username),
            settingsPage.is_bio_equal(bio),
            settingsPage.is_email_equal(email)
            ])
            self.logger.info("기대 결과 2 - 입력한 값이 입력 필드에 입력됨")

            settingsPage.click_update_btn()
            print(f"header url = {header.get_profile_img()}")
            print(f"header username = {header.get_username()}")
            print(f"url = {url}")
            print(f"username = {username}")
            assert all([
                url in header.get_profile_img(),
                header.get_username() == username
            ])
            self.logger.info("기대 결과 3 - 프로필 사진과 계정명이 헤더에 노출됨")
            self.logger.info("회원 정보 입력 및 제출 완료")
        except Exception as e:
            self.logger.error(f"❌ 회원 정보 업데이트 테스트 중 오류 발생: {e}")
            assert False, "❌ 회원 정보 업데이트 테스트 중 오류 발생"
        finally:
            update("User", {"username":"user1", "email":"1@1.1"}, {"username":username}) # 테스트 종료 후 username, email 정보 초기화