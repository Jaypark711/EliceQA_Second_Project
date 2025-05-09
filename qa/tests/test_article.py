import pytest
from pages.body.home_page import HomePage
from pages.body.signin_page import SignInPage
from pages.body.article_page import ArticlePage
import time


@pytest.mark.usefixtures("driver")
class TestAriclePage:
    def test_del_tags(self, driver):
        homePage = HomePage(driver)
        signInPage = SignInPage(driver)
        articlePage = ArticlePage(driver)

        homePage.click_sign_in_link()
        signInPage.login()
        homePage.click_new_post_link()
        title = "타이틀xkdldldk"
        description = "디스크립션"
        body = "바디\n바디"
        tags = ("태그1", "태그2")
        articlePage.save_article(title, description, body, tags)
        time.sleep(2)
