import pytest
from db.db_utils import *
from config.config import BASE_URL
from utils.logger import setupLogger
from pages.header.header import Header
from pages.body.home_page import HomePage
from pages.body.signin_page import SignInPage
from pages.body.article_page import ArticlePage
from selenium.webdriver.remote.webdriver import WebDriver


@pytest.mark.usefixtures("driver")
class TestAriclePage:
    logger = setupLogger(__qualname__)

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, driver: WebDriver):
        init_db() # 테스트 환경 초기화
        driver.get(BASE_URL)

        yield

        self.logger.info("==================================")
