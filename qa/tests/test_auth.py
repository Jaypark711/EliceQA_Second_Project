import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage

@pytest.mark.usefixtures("driver")
class TestAuthentication:
    def test_successful_login(self, driver):
        pass