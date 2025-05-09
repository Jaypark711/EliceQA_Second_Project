import pytest

from utils.logger import setupLogger
from pages.home_page import HomePage
from pages.login_page import LoginPage

@pytest.mark.usefixtures("driver")
class TestAuthentication:
    logger = setupLogger(__qualname__)

    def test_successful_signup(self, driver):
        """AUTH_01: 유효한 정보로 회원가입 성공"""
        self.logger.info("회원가입 테스트 시작")

    def test_successful_login(self, driver):
        """AUTH_02: 유효한 정보로 로그인 성공 및 사용자 정보 확인"""
        self.logger.info("로그인 테스트 시작")

    def test_login_fail(self, driver):
        """AUTH_03: 잘못된 정보로 로그인 시 오류 메시지 제공 확인"""
        
    def test_logout(self, driver):
        """AUTH_04: 로그인 상태에서 로그아웃 성공"""
        self.logger.info("로그아웃 테스트 시작")