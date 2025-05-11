import pytest

from config.config import BASE_URL
from pages.header.header import Header
from pages.body.signin_page import SignInPage
from pages.body.home_page import HomePage
from utils.logger import setupLogger

@pytest.mark.usefixtures("driver")
class TestFilter():
    logger = setupLogger(__qualname__)

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, driver):
        driver.get(BASE_URL)
        yield
        self.logger.info("==================================")

    def test_filter_articles_by_tag(self, driver):
        """FILTER_01: 태그 선택 시 해당 태그를 포함한 게시글만 필터링되어 표시되는지 확인"""
        self.logger.info("태그 선택 및 게시글 필터링 테스트 시작")
        header = Header(driver)
        signInPage = SignInPage(driver)
        home = HomePage(driver)

        try:
            header.click_sign_in_link()
            signInPage.login()

            clicked_tag_text = home.click_random_popular_tag_link()
            self.logger.info("인기 태그 목록에서 무작위 태그 클릭 및 해당 태그 텍스트 추출 완료")

            tag_tab_text = home.get_tag_tab_link_text()
            self.logger.info("화면에 표시된 태그 탭 텍스트 추출 완료")

            assert clicked_tag_text == tag_tab_text
            self.logger.info("클릭한 인기 태그와 화면에 표시된 태그 탭 텍스트가 일치함을 확인")

            # TODO: 태그를 포함한 게시글 필터링 확인 (게시글 정보 불러오는 함수 구현 전까지 대기)

        except Exception as e:
            self.logger.error(f"❌ FILTER_01 테스트 중 오류 발생: {e}")
            assert False

    # def test_popular_tags_update_correctly(self):
    #     """FILTER_02: Popular Tags가 게시글 태그 등록 상황에 따라 정확히 반영되는지 확인"""