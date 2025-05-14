import allure
import time
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from config.config import BASE_URL
from data.user_data import VALID_USER, SETTING_USER_1, SETTING_USER_2, SETTING_USER_3
from pages.home_page import HomePage
from pages.sign_in_page import SignInPage
from pages.sign_up_page import SignUpPage
from pages.settings_page import SettingsPage
from utils.logger import setupLogger
from db.db_utils import init_db

@allure.suite("test_settings.py")
@allure.sub_suite("SETTING TEST")
@pytest.mark.usefixtures("driver")
class TestSettings:
    logger = setupLogger(__qualname__)

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, driver:WebDriver):
        init_db() # 테스트 환경 초기화: 상태 의존성을 제거하고 동일한 초기 조건 보장
        driver.get(BASE_URL)

        yield

        self.logger.info("=================================================================")

    @allure.title("[SETTING_01]: 설정 - 정보 수정")
    @allure.description("사용자 정보 업데이트 성공 확인")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("user_data", [SETTING_USER_1, SETTING_USER_2, SETTING_USER_3])
    def test_update_user_info_successfully(self, driver, user_data):
        self.logger.info("▶️ 회원 정보 업데이트 테스트 시작")

        homePage = HomePage(driver)
        signUpPage = SignUpPage(driver)
        settingsPage = SettingsPage(driver)

        try:
            # 테스트 환경 세팅
            homePage.header.click_sign_up_link()
            signUpPage.sign_up.sign_up()

            # 테스트 시나리오 시작
            signUpPage.header.click_settings_link()
            assert settingsPage.header.is_go_to_settings_page()
            self.logger.info("✅ 기대 결과 1: Settings 페이지로 진입됨")

            settingsPage.settings.change_user_info(url = user_data["url"], username = user_data["username"], bio = user_data["bio"], email = user_data["email"])
            assert all([ 
                settingsPage.settings.get_url_link_input_value() == user_data["url"],
                settingsPage.settings.get_username_input_value() == user_data["username"], 
                settingsPage.settings.get_bio_input_value() == user_data["bio"],
                settingsPage.settings.get_email_input_value() == user_data["email"]
            ])
            self.logger.info("✅ 기대 결과 2: 입력한 이미지링크 값이 'URL of profile picture' 입력 필드에 정상 반영됨")
            self.logger.info("✅ 기대 결과 3: 입력한 유저명 값이 'Username' 입력 필드에 정상 반영됨")
            self.logger.info("✅ 기대 결과 4: 입력한 간단설명 값이 입력 필드에 입력됨")
            self.logger.info("✅ 기대 결과 5: 입력한 이메일 값이 입력 필드에 입력됨")
            
            settingsPage.settings.click_update_btn()
            assert all([
                user_data["url"] in homePage.header.get_profile_img(),
                user_data["username"] == homePage.header.get_username()
            ])
            self.logger.info(f"✅ 기대 결과 6: 업데이트 후 Header - [마이프로필] 영역에 {user_data['url']} 와 {user_data['username']}이 노출됨")
            self.logger.info("🎉 회원 정보 입력 및 제출 완료")

        except Exception as e:
            self.logger.error(f"❌ SETTING_01 테스트 중 오류 발생: {e}")
            assert False, "❌ SETTING_01 테스트 중 오류 발생"


    @allure.title("[SETTING_02]: 설정 - 비밀번호 수정")
    @allure.description("비밀번호 변경 성공 확인 (로그아웃 후 새 비밀번호로 로그인)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("user_data", [SETTING_USER_1, SETTING_USER_2, SETTING_USER_3])
    def test_update_user_password_successfully(self,driver,user_data):
        self.logger.info("▶️ 비밀번호 업데이트 테스트 시작")

        homePage = HomePage(driver)
        signInPage = SignInPage(driver)
        signupPage = SignUpPage(driver)
        settingsPage = SettingsPage(driver)
        
        try:
            # 테스트 환경 세팅
            homePage.header.click_sign_up_link()
            signupPage.sign_up.sign_up()

            # 테스트 시나리오 시작
            signupPage.header.click_settings_link()
            assert settingsPage.header.is_go_to_settings_page()
            self.logger.info("✅ 기대 결과 1: Settings 페이지로 진입됨")

            settingsPage.settings.change_user_info(password=user_data["password"])
            assert settingsPage.settings.get_password_input_value() == user_data["password"]
            self.logger.info("✅ 기대 결과 2: 입력한 값이 입력 필드에 입력됨")

            settingsPage.settings.click_update_btn()

            time.sleep(1) # 대기 필수
            settingsPage.header.click_settings_link()

            settingsPage.settings.click_logout_btn()

            homePage.header.click_sign_in_link()
            signInPage.sign_in.send_email_input(VALID_USER["email"])
            signInPage.sign_in.send_password_input(user_data["password"])
            signInPage.sign_in.click_sign_in_btn()

            assert homePage.header.is_my_profile_link_appear()
            self.logger.info(f"✅ 기대 결과 3: 변경된 비밀번호 {user_data[‘password’]}로 로그인 됨")
            self.logger.info("🎉 비밀번호 업데이트 테스트 완료")

        except Exception as e:
            self.logger.error(f"❌ SETTING_02 테스트 중 오류 발생: {e}")
            assert False, "❌ SETTING_02 테스트 중 오류 발생"
