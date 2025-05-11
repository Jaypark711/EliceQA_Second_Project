import pytest
from config.config import BASE_URL
from utils.logger import setupLogger
from pages.header.header import Header
from pages.body.home_page import HomePage
from pages.body.signin_page import SignInPage
from pages.body.article_page import ArticlePage
import time


@pytest.mark.usefixtures("driver")
class TestAriclePage:
    logger = setupLogger(__qualname__)

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, driver):
        driver.get(BASE_URL)

        yield

        self.logger.info("==================================")