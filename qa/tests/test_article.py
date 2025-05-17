import allure
import pytest
from selenium.webdriver.remote.webelement import WebElement

from config.config import BASE_URL
from data.user_data import VALID_USER
from data.dummy_data import ARTICLE_DATA_1, ARTICLE_DATA_2
from pages.home_page import HomePage
from pages.sign_up_page import SignUpPage
from pages.editor_page import EditorPage
from utils.helpers import Helpers
from utils.logger import setupLogger
from db.db_utils import init_db, run_prisma_seed, get_user_id_by_username, get_articles_by_title, get_article_details_by_slug

@allure.suite("test_article.py")
@allure.sub_suite("ARTICLE TEST")
@pytest.mark.usefixtures("driver")
class TestAriclePage:
    logger = setupLogger(__qualname__)

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, driver):
        init_db()  # 테스트 환경 초기화
        driver.get(BASE_URL)

        yield

        self.logger.info("=================================================================")

    @allure.title("[ARTICLE_01]: 게시글 - 신규 등록")
    @allure.description("로그인 후 새 게시글 작성 및 게시 성공 확인 (제목, 본문, 태그 포함)") 
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("input_title, input_desc, input_body, input_tags", [ARTICLE_DATA_1])
    def test_save_new_article(self, driver, input_title, input_desc, input_body, input_tags):
        self.logger.info("▶️ 신규 Article 등록 테스트 시작")

        homePage = HomePage(driver)
        signupPage = SignUpPage(driver)
        editorPage = EditorPage(driver)

        try:
            # 테스트 환경 세팅
            homePage.header.click_sign_up_link()
            signupPage.sign_up.sign_up()

            # 테스트 시나리오 시작
            homePage.header.click_new_post_link()
            editorPage.editor.save_article(input_title, input_desc, input_body, input_tags)
            saved_article = homePage.article.load_article_details()

            # 비교용 slug 생성을 위해 DB에서 유저 키 값 받아오기
            user_id = get_user_id_by_username(VALID_USER["username"])
            new_slug = homePage.article.get_article_slug(input_title, user_id)

            # 현재 url과 제목 값 기반으로 만들어진 url과 비교
            assert driver.current_url == BASE_URL + new_slug
            self.logger.info("✅ 기대 결과 1 : 현재 URL이 제목 값에 따라 정상 생성됨")

            # 저장된 제목과 실제 입력한 제목 비교
            assert saved_article["title"] == input_title
            self.logger.info("✅ 기대 결과 2 : 신규 게시글 제목이 입력한 값으로 정상 저장됨")

            # 저장된 본문 내용과 실제 입력한 본문 내용 비교
            assert saved_article["body"] == input_body
            self.logger.info("✅ 기대 결과 3 : 신규 게시글 본문 내용이 입력한 값으로 정상 저장됨")

            # 저장된 태그들 값과 실제 입력한 태그들 값 비교
            assert saved_article["tags"] == input_tags
            self.logger.info("✅ 기대 결과 4 : 신규 게시글 태그가 입력한 값으로 정상 저장됨")

            # 게시글이 DB에 정말로 저장되었는지 확인 (By. title)
            assert get_articles_by_title(saved_article["title"]) != None
            self.logger.info("✅ 기대 결과 5 : 신규 게시글 제목으로 DB 조회 시 해당 글이 정상적으로 조회됨")
            self.logger.info("🎉 신규 Article 등록 테스트 성공")

        except Exception as e:
            self.logger.error(f"❌ ARTICLE_01 테스트 중 오류 발생: {e}")
            assert False, "❌ ARTICLE_01 테스트 중 오류 발생"

    @allure.title("[ARTICLE_02]: 게시글 - 조회")
    @allure.description("게시글 목록(Global Feed) 게시글 표시 확인") 
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("input_title, input_desc, input_body, input_tags", [ARTICLE_DATA_1])
    def test_load_article_previews(self, driver, input_title, input_desc, input_body, input_tags):
        self.logger.info("▶️ Global Feed 게시글 목록 표시 확인 테스트 시작")

        homePage = HomePage(driver)
        signupPage = SignUpPage(driver)
        editorPage = EditorPage(driver)
        helpers = Helpers(driver)

        try:
            # 테스트 환경 세팅
            homePage.header.click_sign_up_link()
            signupPage.sign_up.sign_up()

            # 테스트 시나리오 시작
            homePage.tabs.click_global_feed_tab_link()
            helpers.wait_until_page_load_complete()
            article_preview_lists = homePage.article.load_article_preview_lists()

            # 게시글 목록이 없을 경우
            if type(article_preview_lists) == WebElement:
                assert homePage.article.is_empty_text_div_show()
                self.logger.info("✅ 기대 결과 1 : 게시글 없을 시 Empty 문구 정상 제공 확인")

            # Empty 문구 확인 후 신규 글 작성
            homePage.header.click_new_post_link()

            editorPage.editor.save_article(input_title, input_desc, input_body, input_tags)

            editorPage.header.click_home_link()
            homePage.tabs.click_global_feed_tab_link()

            helpers.wait_until_page_load_complete()
            article_preview_lists = homePage.article.load_article_preview_lists()

            # 게시글이 존재한다면 DB 저장 여부를 확인할 타이틀 값만 추출
            if len(article_preview_lists) != 0:
                preview_titles = []
                for preview in article_preview_lists.values():
                    if isinstance(preview, dict) and "title" in preview:
                        preview_titles.append(preview["title"])

            # 게시글 목록이 있을 경우 - 실제 DB에 등록된 게시글인지 확인
            for title in preview_titles:
                assert get_articles_by_title(title) != None
                self.logger.info("✅ 기대 결과 2 : 게시글 있을 시 DB에서 정상적으로 게시글 목록 로드 확인")
            self.logger.info("🎉 Global Feed 게시글 목록 표시 확인 테스트 성공")

        except Exception as e:
            self.logger.error(f"❌ ARTICLE_02 테스트 중 오류 발생: {e}")
            assert False, "❌ ARTICLE_02 테스트 중 오류 발생"

    @allure.title("[ARTICLE_03]: 게시글 - 상세 페이지")
    @allure.description("특정 게시글 상세 페이지 접근 및 내용(제목, 본문) 확인") 
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("input_title, input_desc, input_body, input_tags", [ARTICLE_DATA_1])
    def test_confirm_article_detail(self, driver, input_title, input_desc, input_body, input_tags):
        self.logger.info("▶️ 특정 게시글의 상세 페이지 접근 및 내용(제목, 본문) 확인 테스트 시작")

        homePage = HomePage(driver)
        signupPage = SignUpPage(driver)
        editorPage = EditorPage(driver)

        try:
            # 테스트 환경 세팅
            homePage.header.click_sign_up_link()
            signupPage.sign_up.sign_up()

            # 테스트 시나리오 시작
            homePage.header.click_new_post_link()
            editorPage.editor.save_article(input_title, input_desc, input_body, input_tags)

            editorPage.header.click_home_link()

            # 다른 계정 글 확인용 dummy 데이터 삽입하기
            run_prisma_seed()

            # 다른 계정이 쓴 글 진입 (dummy)
            homePage.tabs.click_global_feed_tab_link()
            homePage.article.click_article(0, 1)
            others_slug = driver.current_url.replace(f"{BASE_URL}article/", "")
            others_article = homePage.article.load_article_details()

            others_db_article_datas = get_article_details_by_slug(others_slug)
            assert others_db_article_datas[2] == others_article["title"]
            self.logger.info("✅ 기대 결과 1 : 다른 계정의 글 제목 내용 확인")

            assert others_db_article_datas[4] == others_article["body"]
            self.logger.info("✅ 기대 결과 2 : 다른 계정의 글 본문 내용 확인")

            assert homePage.article.is_not_my_article() == True
            self.logger.info("✅ 기대 결과 3 : 다른 계정이 쓴 글 수정 및 삭제 불가 확인")

            # 현재 유저가 쓴 글 진입
            homePage.header.click_home_link()
            homePage.tabs.click_global_feed_tab_link()
            homePage.article.click_article(0, len(homePage.article.load_article_preview_lists()))

            my_slug = driver.current_url.replace(f"{BASE_URL}article/", "")
            my_article = homePage.article.load_article_details()

            my_db_article_datas = get_article_details_by_slug(my_slug)

            assert my_db_article_datas[2] == my_article["title"]
            self.logger.info("✅ 기대 결과 4 : 내가 쓴 글 글 제목 내용 확인")

            assert my_db_article_datas[4] == my_article["body"]
            self.logger.info("✅ 기대 결과 5 : 내가 쓴 글 본문 내용 확인")

            assert homePage.article.is_my_article() == True
            self.logger.info("✅ 기대 결과 6 : 내 계정이 쓴 글 수정 및 삭제 가능함 확인")
            self.logger.info("🎉 특정 게시글의 상세 페이지 접근 및 내용(제목, 본문) 확인 테스트 성공")

        except Exception as e:
            self.logger.error(f"❌ ARTICLE_03 테스트 중 오류 발생: {e}")
            assert False, "❌ ARTICLE_03 테스트 중 오류 발생"

    @allure.title("[ARTICLE_04]: 게시글 - 수정")
    @allure.description("자신이 작성한 게시글 수정 성공 확인") 
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("input_title, input_desc, input_body, input_tags, modi_title, modi_desc, modi_body, modi_tags", [(*ARTICLE_DATA_1, *ARTICLE_DATA_2)])
    def test_modi_my_article(self, driver, input_title, input_desc, input_body, input_tags, modi_title, modi_desc, modi_body, modi_tags):
        self.logger.info("▶️ 내가 작성한 게시글 수정 테스트 시작")

        homePage = HomePage(driver)
        signupPage = SignUpPage(driver)
        editorPage = EditorPage(driver)

        try:
            # 테스트 환경 세팅
            homePage.header.click_sign_up_link()
            signupPage.sign_up.sign_up()

            # 테스트 시나리오 시작
            homePage.header.click_new_post_link()
            editorPage.editor.save_article(input_title, input_desc, input_body, input_tags)

            # 글 상세 화면에서 수정 버튼 선택
            homePage.article.click_edit_article_btn()

            # 수정 화면에서 글 내용 변경 후 저장
            editorPage.editor.delete_selected_tags([input_tags[0]])
            editorPage.editor.save_article(modi_title, modi_desc, modi_body, modi_tags)

            # *글 상세 화면에서 변경 내용 확인
            modified_article = homePage.article.load_article_details()

            # 변경될 slug 확인을 위해 user_id 추출
            user_id = get_user_id_by_username(VALID_USER["username"])
            new_slug = homePage.article.get_article_slug(modi_title, user_id)

            # 현재 url과 제목 값 기반으로 만들어진 url과 비교
            assert driver.current_url == BASE_URL + new_slug
            self.logger.info("✅ 기대 결과 1 : 현재 URL이 수정된 제목 값에 따라 정상 변경됨")

            # 저장된 제목과 실제 입력한 제목 비교
            assert modified_article["title"] == modi_title
            self.logger.info("✅ 기대 결과 2 : 게시글 제목이 수정한 값으로 정상 저장됨")

            # 저장된 본문 내용과 실제 입력한 본문 내용 비교
            assert modified_article["body"] == modi_body
            self.logger.info("✅ 기대 결과 3 : 게시글 본문 내용이 수정한 값으로 정상 저장됨")

            # 저장된 태그들 값과 실제 입력한 태그들 값 비교
            modi_tags.insert(
                0, input_tags[1]
            )  # 삭제하지 않은 태그 값 비교를 위해 리스트에 추가
            assert modified_article["tags"] == modi_tags
            self.logger.info("✅ 기대 결과 4 : 게시글 태그가 수정한 값으로 정상 저장됨")

            # 게시글이 DB에 정말로 저장되었는지 확인 (By. title)
            assert get_articles_by_title(modified_article["title"]) != None
            self.logger.info("✅ 기대 결과 5 : 변경된 게시글 제목으로 DB 조회 시 해당 글이 정상적으로 조회됨")
            self.logger.info("🎉 내가 작성한 게시글 수정 테스트 성공")

        except Exception as e:
            self.logger.error(f"❌ ARTICLE_04 테스트 중 오류 발생: {e}")
            assert False, "❌ ARTICLE_04 테스트 중 오류 발생"

    @allure.title("[ARTICLE_05]: 게시글 - 삭제")
    @allure.description("자신이 작성한 게시글 삭제 성공 확인") 
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("input_title, input_desc, input_body, input_tags", [ARTICLE_DATA_1])
    def test_del_my_article(self, driver, input_title, input_desc, input_body, input_tags):
        self.logger.info("▶️ 내가 작성한 게시글 삭제 테스트 시작")

        homePage = HomePage(driver)
        signupPage = SignUpPage(driver)
        editorPage = EditorPage(driver)

        try:
            # 테스트 환경 세팅
            homePage.header.click_sign_up_link()
            signupPage.sign_up.sign_up()

            # 테스트 시나리오 시작
            homePage.header.click_new_post_link()
            editorPage.editor.save_article(input_title, input_desc, input_body, input_tags)
            saved_article = homePage.article.load_article_details()

            homePage.article.click_delete_article_btn()

            # DB에서 글 삭제 되었는지 확인하기
            assert get_articles_by_title(saved_article["title"]) == None
            self.logger.info("✅ 기대 결과 1 : 삭제 진행한 게시글 제목으로 DB 조회 시 해당 글 조회되지 않음 확인")
            self.logger.info("🎉 내가 작성한 게시글 삭제 테스트 성공")

        except Exception as e:
            self.logger.error(f"❌ ARTICLE_05 테스트 중 오류 발생: {e}")
            assert False, "❌ ARTICLE_05 테스트 중 오류 발생"