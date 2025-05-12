import pytest

from config.config import BASE_URL
from pages.header.header import Header
from pages.body.signup_page import SignUpPage
from pages.body.home_page import HomePage
from pages.body.article_page import ArticlePage
from utils.logger import setupLogger
from db.db_utils import delete_all_user, run_prisma_seed, get_article_count_by_tag_name

@pytest.mark.usefixtures("driver")
class TestFilter():
    logger = setupLogger(__qualname__)

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, driver):
        delete_all_user() # 테스트 환경 초기화: 상태 의존성을 제거하고 동일한 초기 조건 보장
        run_prisma_seed() # 초기 데이터 생성
        driver.get(BASE_URL)

        yield

        self.logger.info("==================================")

    def test_filter_articles_by_tag(self, driver):
        """FILTER_01: 태그 선택 시 해당 태그를 포함한 게시글만 필터링되어 표시되는지 확인"""
        self.logger.info("태그 선택 및 게시글 필터링 테스트 시작")
        header = Header(driver)
        home = HomePage(driver)
        signUpPage = SignUpPage(driver)
        articlePage = ArticlePage(driver)

        try:
            # 테스트 환경 세팅
            header.click_sign_up_link()
            signUpPage.sign_up()

            # 테스트 시나리오 시작
            clicked_tag_text = home.click_random_popular_tag_link()
            self.logger.info("인기 태그 목록에서 무작위 태그 클릭 및 해당 태그 텍스트 추출 완료")

            tag_tab_text = home.get_tag_tab_link_text()
            self.logger.info("화면에 표시된 태그 탭 텍스트 추출 완료")

            assert clicked_tag_text == tag_tab_text # 기대 결과 1: 선택된 태그와 이름이 동일한 탭이 Global Feed 우측에 추가되어야 함
            self.logger.info("클릭한 인기 태그와 화면에 표시된 태그 탭 텍스트가 일치함을 확인")

            articles = articlePage.load_article_preview_lists()
            for article_id, article_data in articles.items():
                assert clicked_tag_text in article_data["tags"] # 기대 결과 2: 태그가 포함된 게시글만 필터링되어 표시되어야 함
            self.logger.info("클릭한 태그를 포함한 게시글만 필터링되어 표시됨을 확인")

        except Exception as e:
            self.logger.error(f"❌ FILTER_01 테스트 중 오류 발생: {e}")
            assert False

    def test_popular_tags_update_correctly(self, driver):
        """FILTER_02: Popular Tags가 게시글 태그 등록 상황에 따라 정확히 반영되는지 확인"""
        self.logger.info("태그 등록 상황에 따른 순위 반영 테스트 시작")
        header = Header(driver)
        home = HomePage(driver)
        signUpPage = SignUpPage(driver)

        try:
            # 테스트 환경 세팅
            header.click_sign_up_link()
            signUpPage.sign_up()
            
            # 테스트 시나리오 시작
            popular_tag_texts = home.get_popular_tag_texts()
            self.logger.info("인기 태그 목록에서 태그 텍스트 추출 완료")

            prev_count = None
            for tag_text in popular_tag_texts:
                current_count = get_article_count_by_tag_name(tag_text)

                if prev_count is not None and current_count > prev_count:
                    assert False
                prev_count = current_count
            assert True # 기대 결과 1: Popular Tags가 게시글 태그 등록 상황에 따라 정확하게 반영되어야 함
            self.logger.info("태그 순위가 게시글 수 기준으로 정확하게 반영됨")

        except Exception as e:
            self.logger.error(f"❌ FILTER_02 테스트 중 오류 발생: {e}")
            assert False