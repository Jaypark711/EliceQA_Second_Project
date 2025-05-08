import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage

@pytest.mark.usefixtures("driver")
class TestAuthentication:
    def test_login(self, driver):
        homePage = HomePage(driver)
        loginPage = LoginPage(driver)

        homePage.click_sign_in_link()
        loginPage.login()

    # def test_successful_login(self, driver):
    #     loginPage = LoginPage(driver)
        
    #     # 여기는 login 호출 X -> 직접 요소에 값 입력