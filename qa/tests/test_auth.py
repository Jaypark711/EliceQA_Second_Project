import allure
import pytest

from config.config import BASE_URL
from data.user_data import VALID_USER 
from pages.header.header import Header
from pages.body.home_page import HomePage
from pages.body.signup_page import SignUpPage
from pages.body.signin_page import SignInPage
from pages.body.settings_page import SettingsPage
from utils.logger import setupLogger
from db.db_utils import init_db

@allure.suite("test_auth.py")
@allure.sub_suite("AUTH TEST")
@pytest.mark.usefixtures("driver")
class TestAuthentication:
    logger = setupLogger(__qualname__)

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, driver):
        init_db() # 테스트 환경 초기화: 상태 의존성을 제거하고 동일한 초기 조건 보장
        driver.get(BASE_URL)

        yield

        self.logger.info("==================================")

    @allure.title("[AUTH_01]: 인증 - 회원가입")
    @allure.description("유효한 정보로 회원가입 성공 및 사용자 정보 확인")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_signup(self, driver):
        self.logger.info("회원가입 테스트 시작")
        header = Header(driver)
        homePage = HomePage(driver)
        signUpPage = SignUpPage(driver)

        try:
            header.click_sign_up_link()
            assert header.is_go_to_sign_up_page() # 기대 결과 1: Sign up 페이지로 진입되어야 함

            signUpPage.send_username_input(VALID_USER["username"])
            assert signUpPage.get_username_input_value() == VALID_USER["username"] # 기대 결과 2: {사용자명}이 "Username" 입력 필드에 정상 반영됨

            signUpPage.send_email_input(VALID_USER["email"])
            assert signUpPage.get_email_input_value() == VALID_USER["email"] # 기대 결과 3: {이메일}이 "Email" 입력 필드에 정상 반영됨

            signUpPage.send_password_input(VALID_USER["password"])
            assert signUpPage.get_password_input_value() == VALID_USER["password"] # 기대 결과 4: {비밀번호}가 "Password" 입력 필드에 정상 반영됨
        
            signUpPage.click_sign_up_btn()
            assert header.is_go_to_home_page() # 기대 결과 5: 메인 화면 진입  
            self.logger.info("회원가입 정보 입력 및 제출 완료")

            assert all([ # 기대 결과 6: 메인 화면에 Your Feed 탭, New Post 링크, Settings 링크, MyProfile 링크 추가 표시
                homePage.is_your_feed_tab_link_appear(),
                header.is_new_post_link_appear(),
                header.is_settings_link_appear(),
                header.is_my_profile_link_appear()
            ])
            self.logger.info("사용자 정보 확인 완료")
            self.logger.info("유효한 정보로 회원가입 테스트 성공")
        except Exception as e:
            self.logger.error(f"❌ AUTH_01 테스트 중 오류 발생: {e}")
            assert False, "❌ AUTH_01 테스트 중 오류 발생"

    @allure.title("[AUTH_02]: 인증 - 회원가입")
    @allure.description("잘못된 정보로 회원가입 시 오류 메시지 제공 확인")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("username, email, password, expected_result, description", [ # TODO: 데이터 임시 하드코딩 (추후 분리하기)
        ("", "", "", "email can't be blank", "사용자명, 이메일, 비밀번호 입력창을 모두 공백"),
        (VALID_USER["username"], "", "", "email can't be blank", "이메일, 비밀번호 입력창을 공백"),
        (VALID_USER["username"], VALID_USER["email"], "", "password can't be blank", "비밀번호 입력창을 공백"),
        (VALID_USER["username"], VALID_USER["email"], VALID_USER["password"], ["email has already been taken", "username has already been taken"], "유효한 입력값")
    ])
    def test_fail_signup(self, driver, username, email, password, expected_result, description):
        self.logger.info(f"{description}(으)로 회원가입 테스트 시작")
        header = Header(driver)
        signInPage = SignInPage(driver)
        signUpPage = SignUpPage(driver)
        settingsPage = SettingsPage(driver)
        
        try:
            # 테스트 환경 세팅
            header.click_sign_up_link()
            signUpPage.sign_up()
            header.click_settings_link()
            settingsPage.click_logout_btn()

            # 테스트 시나리오 시작
            header.click_sign_up_link()
            assert header.is_go_to_sign_up_page() # 기대 결과 1: Sign up 페이지로 진입되어야 함

            signUpPage.send_username_input(username)
            assert signUpPage.get_username_input_value() == username # 기대 결과 2: {사용자명}이 "Username" 입력 필드에 정상 반영됨

            signUpPage.send_email_input(email)
            assert signUpPage.get_email_input_value() == email # 기대 결과 3: {이메일}이 "Email" 입력 필드에 정상 반영됨

            signUpPage.send_password_input(password)
            assert signUpPage.get_password_input_value() == password # 기대 결과 4: {비밀번호}가 "Password" 입력 필드에 정상 반영됨

            signUpPage.click_sign_up_btn()
            if isinstance(expected_result, str):
                assert expected_result in signUpPage.get_error_message_text() # 기대 결과 5: {경고창}이 표시됨
            else:
                assert set(signUpPage.get_error_messages_text()) == set(expected_result) # 기대 결과 5: {경고창}이 표시됨
            self.logger.info(f"{description}(으)로 회원가입 테스트 시 {expected_result} 경고창 출력 확인")

        except Exception as e:
            self.logger.error(f"❌ AUTH_02 테스트 중 오류 발생: {e}")
            assert False, "❌ AUTH_02 테스트 중 오류 발생"

    @allure.title("[AUTH_03]: 인증 - 로그인")
    @allure.description("유효한 정보로 로그인 성공 및 사용자 정보 확인")
    @allure.severity(allure.severity_level.NORMAL)
    def test_successful_signin(self, driver):
        self.logger.info("유효한 정보로 로그인 테스트 시작")
        header = Header(driver)
        homePage = HomePage(driver)
        signInPage = SignInPage(driver)
        signUpPage = SignUpPage(driver)
        settingsPage = SettingsPage(driver)

        try:
            # 테스트 환경 세팅
            header.click_sign_up_link()
            signUpPage.sign_up()
            header.click_settings_link()
            settingsPage.click_logout_btn()

            # 테스트 시나리오 시작
            header.click_sign_in_link()
            assert header.is_go_to_sign_in_page() # 기대 결과 1: Sign in 페이지로 진입되어야 함

            signInPage.send_email_input(VALID_USER["email"])
            assert signInPage.get_email_input_value() == VALID_USER["email"] # 기대 결과 2: {이메일}이 "Email" 입력 필드에 정상 반영됨

            signInPage.send_password_input(VALID_USER["password"])
            assert signInPage.get_password_input_value() == VALID_USER["password"] # 기대 결과 3: {비밀번호}가 "Password" 입력 필드에 정상 반영됨

            signInPage.click_sign_in_btn()
            assert header.is_go_to_home_page() # 기대 결과 4: 메인 화면 진입  
            self.logger.info("로그인 정보 입력 및 제출 완료")

            assert all([ # 기대 결과 5: 메인 화면에 Your Feed 탭, New Post 링크, Settings 링크, MyProfile 링크 추가 표시
                homePage.is_your_feed_tab_link_appear(),
                header.is_new_post_link_appear(),
                header.is_settings_link_appear(),
                header.is_my_profile_link_appear()
            ])
            self.logger.info("사용자 정보 확인 완료")
            self.logger.info("유효한 정보로 로그인 테스트 성공")

        except Exception as e:
            self.logger.error(f"❌ AUTH_03 테스트 중 오류 발생: {e}")
            assert False, "❌ AUTH_03 테스트 중 오류 발생"

    @allure.title("[AUTH_04]: 인증 - 로그인")
    @allure.description("잘못된 정보로 로그인 시 오류 메시지 제공 확인")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("email, password, expected_result, description", [ # TODO: 데이터 임시 하드코딩 (추후 분리하기)
        ("", "", "email can't be blank", "이메일 및 비밀번호 입력창 모두 공백"),
        ("", VALID_USER["password"], "email can't be blank", "이메일 입력창을 공백"),
        (VALID_USER["email"], "", "password can't be blank", "비밀번호 입력창을 공백"),
        (VALID_USER["email"], "wrong_password", "email or password is invalid", "맞지 않는 비밀번호"),
        ("wrong@email.com", VALID_USER["password"], "email or password is invalid", "미가입 이메일")
    ])
    def test_fail_signin(self, driver, email, password, expected_result, description):
        self.logger.info(f"{description}(으)로 로그인 테스트 시작")
        header = Header(driver)
        signInPage = SignInPage(driver)
        signUpPage = SignUpPage(driver)
        settingsPage = SettingsPage(driver)
        
        try:
            # 테스트 환경 세팅
            header.click_sign_up_link()
            signUpPage.sign_up()
            header.click_settings_link()
            settingsPage.click_logout_btn()

            # 테스트 시나리오 시작
            header.click_sign_in_link()
            assert header.is_go_to_sign_in_page() # 기대 결과 1: Sign in 페이지로 진입되어야 함

            signInPage.send_email_input(email)
            assert signInPage.get_email_input_value() == email # 기대 결과 2: {이메일}이 "Email" 입력 필드에 정상 반영됨

            signInPage.send_password_input(password)
            assert signInPage.get_password_input_value() == password # 기대 결과 3: {비밀번호}가 "Password" 입력 필드에 정상 반영됨

            signInPage.click_sign_in_btn()
            assert signInPage.get_error_messages_text() == expected_result # 기대 결과 4: {경고창}이 표시됨
            self.logger.info(f"{description}(으)로 로그인 테스트 시 {expected_result} 경고창 출력 확인")

        except Exception as e:
            self.logger.error(f"❌ AUTH_04 테스트 중 오류 발생: {e}")
            assert False, "❌ AUTH_04 테스트 중 오류 발생"

    @allure.title("[AUTH_05]: 인증 - 이메일 포맷")
    @allure.description("유효하지 않은 이메일 형식 입력 시 브라우저의 유효성 검사 메시지가 제공되는지 확인")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("email, expected_result", [ # TODO: 데이터 임시 하드코딩 (추후 분리하기)
        ("user", "이메일 주소에 '@'를 포함해 주세요. 'user'에 '@'가 없습니다."),
        ("@", "'@' 앞 부분을 입력해 주세요. '@'(이)가 완전하지 않습니다."),
        ("user@", "'@' 뒷 부분을 입력해 주세요. 'user@'(이)가 완전하지 않습니다.")
    ])
    def test_email_validation_message(self, driver, email, expected_result):
        self.logger.info("이메일 유효성 검사 메시지 테스트 시작")
        header = Header(driver)
        signInPage = SignInPage(driver)
        signUpPage = SignUpPage(driver)

        try:
            # 테스트 시나리오 시작
            header.click_sign_in_link()
            signInPage.send_email_input(email)
            assert signInPage.get_email_input_value() == email # 기대 결과 1: {이메일}이 "Email" 입력 필드에 정상 반영됨

            signInPage.click_sign_in_btn()
            assert signInPage.get_email_validation_message() == expected_result # 기대 결과 2: {경고창}이 표시됨
            self.logger.info("로그인 페이지에서 이메일 유효성 검사 메시지 확인")

            header.click_sign_up_link()
            signUpPage.send_email_input(email)
            assert signUpPage.get_email_input_value() == email # 기대 결과 3: {이메일}이 "Email" 입력 필드에 정상 반영됨

            signUpPage.click_sign_up_btn()
            assert signUpPage.get_email_validation_message() == expected_result # 기대 결과 4: {경고창}이 표시됨
            self.logger.info("회원가입 페이지에서 이메일 유효성 검사 메시지 확인")
            self.logger.info(f"{email}로 이메일 입력 시 {expected_result} 유효성 검사 메시지 확인 완료")

        except Exception as e:
            self.logger.error(f"❌ AUTH_05 테스트 중 오류 발생: {e}")
            assert False, "❌ AUTH_05 테스트 중 오류 발생"

    @allure.title("[AUTH_06]: 인증 - 리다이렉션")
    @allure.description("회원가입 페이지와 로그인 페이지 간의 리다이렉션 기능 확인")
    @allure.severity(allure.severity_level.NORMAL)
    def test_redirection(self, driver):
        self.logger.info("리다이렉션 테스트 시작")
        header = Header(driver)
        signInPage = SignInPage(driver)
        signUpPage = SignUpPage(driver)

        try:
            # 테스트 시나리오 시작
            header.click_sign_in_link()
            assert header.is_go_to_sign_in_page() # 기대 결과 1: Sign in 페이지로 진입되어야 함
            
            signInPage.click_sign_up_link()
            assert header.is_go_to_sign_up_page() # 기대 결과 2: Sign up 페이지로 진입되어야 함

            signUpPage.click_sign_in_link()
            assert header.is_go_to_sign_in_page() # 기대 결과 3: Sign in 페이지로 진입되어야 함
            self.logger.info("리다이렉션 테스트 성공")

        except Exception as e:
            self.logger.error(f"❌ AUTH_06 테스트 중 오류 발생: {e}")
            assert False, "❌ AUTH_06 테스트 중 오류 발생"

    @allure.title("[AUTH_07]: 인증 - 로그아웃")
    @allure.description("로그인 상태에서 로그아웃 성공")
    def test_logout(self, driver):
        self.logger.info("로그아웃 테스트 시작")
        header = Header(driver)
        homePage = HomePage(driver)
        signUpPage = SignUpPage(driver)
        settingsPage = SettingsPage(driver)

        try:
            # 테스트 환경 세팅
            header.click_sign_up_link()
            signUpPage.sign_up()

            # 테스트 시나리오 시작
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
            self.logger.error(f"❌ AUTH_07 테스트 중 오류 발생: {e}")
            assert False, "❌ AUTH_07 테스트 중 오류 발생"