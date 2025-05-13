import pytest

from config.config import BASE_URL
from data.user_data import VALID_USER
from pages.header.header import Header
from pages.body.home_page import HomePage
from pages.body.signup_page import SignUpPage
from pages.body.profile_page import ProfilePage
from pages.body.article_page import ArticlePage
from pages.body.editor_page import EditorPage
from utils.logger import setupLogger
from db.db_utils import init_db, run_prisma_seed, get_user_info_by_username

@pytest.mark.usefixtures("driver")
class TestMyProfile:
    logger = setupLogger(__qualname__)

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, driver):
        init_db() # 테스트 환경 초기화: 상태 의존성을 제거하고 동일한 초기 조건 보장
        driver.get(BASE_URL)

        yield

        self.logger.info("==================================")

    def test_my_profile_shows_user_info_correctly(self, driver):
        """MYPROFILE_01: 마이프로필에서 사용자 정보가 정확히 반영되는지 확인"""
        self.logger.info("마이프로필에서 사용자 정보 반영 테스트 시작")
        header = Header(driver)
        signUpPage = SignUpPage(driver)
        profilePage = ProfilePage(driver)

        try:
            # 테스트 환경 세팅
            header.click_sign_up_link()
            signUpPage.sign_up()

            # 테스트 시나리오 시작
            header.click_my_profile_link()
            self.logger.info("My Profile 링크 클릭 완료")
            assert header.is_go_to_myprofile_page() # 기대 결과 1: 마이프로필로 진입되어야 함
            self.logger.info("마이프로필 페이지 이동 확인 완료")

            username, profile_img_src, bio_text = get_user_info_by_username(VALID_USER["username"])
            if not bio_text:
                assert all([ # 기대 결과 2: 로그인된 사용자의 유저명, 프로필사진이 표시되어야 함
                    profilePage.get_username_title_text() == username,
                    profilePage.get_profile_img_src() == profile_img_src
                ])
                self.logger.info("로그인된 유저의 유저명, 프로필 사진 표시 확인 완료")
            else: # 기대 결과 2: 로그인된 사용자의 유저명, 프로필사진, 소개가 표시되어야 함
                assert all([
                    profilePage.get_username_title_text() == username,
                    profilePage.get_profile_img_src() == profile_img_src,
                    profilePage.get_bio_p_text() == bio_text
                ])
                self.logger.info("로그인된 유저의 유저명, 프로필 사진, 소개 표시 확인 완료")

        except Exception as e:
            self.logger.error(f"❌ MYPROFILE_01 테스트 중 오류 발생: {e}")
            assert False

    @pytest.mark.parametrize("title, description, body, tags", [ # TODO: 데이터 임시 하드코딩 (추후 분리하기)
        ("제목", "설명", "내용", ["태그"])
    ])
    def test_show_my_articles(self, driver, title, description, body, tags):
        """MYPROFILE_02: 마이프로필에서 내가 작성한 게시글 목록(My Articles) 표시 확인"""
        self.logger.info("마이프로필에서 My Articles 탭 테스트 시작")
        header = Header(driver)
        signUpPage = SignUpPage(driver)
        profilePage = ProfilePage(driver)
        articlePage = ArticlePage(driver)
        editorPage = EditorPage(driver)

        try:
            # 테스트 환경 세팅
            header.click_sign_up_link()
            signUpPage.sign_up()

            # 테스트 시나리오 시작
            header.click_my_profile_link()
            profilePage.click_my_article_tab_link()
            assert all([ # 기대 결과 1: 마이프로필로 진입되어야 하며, My Articles 탭이 자동 선택됨
                header.is_go_to_myprofile_page(),
                profilePage.is_my_article_tab_active()
            ])
            self.logger.info("마이 프로필에서 My Articles 탭 클릭 및 탭 활성화 확인")

            assert articlePage.is_empty_text_div_show() # 기대 결과 2: (등록된 Article X) : "No articles are here... yet." 텍스트가 노출됨
            self.logger.info("등록된 Article이 없는 경우 'No articles are here... yet.' 텍스트 노출 확인")

            header.click_new_post_link()
            editorPage.save_article(title, description, body, tags)

            header.click_my_profile_link()
            first_article = articlePage.load_first_article_data()

            assert all([ # 기대 결과 3: (등록 Article 1개 이상) : 내가 작성한 게시글 목록이 표시되어야 함
                first_article["title"] == title, 
                first_article["description"] == description,
                first_article["tags"] == tags[0],
            ])
            self.logger.info("등록된 Article이 있는 경우 내가 작성한 게시글 목록 표시 확인")

        except Exception as e:
            self.logger.error(f"❌ MYPROFILE_02 테스트 중 오류 발생: {e}")
            assert False

    def test_show_favorited_articles(self, driver):
        """MYPROFILE_03: 마이프로필에서 좋아요 누른 게시글 목록(Favorited Articles) 표시 확인"""
        self.logger.info("마이프로필에서 Favorited Articles 탭 테스트 시작")
        run_prisma_seed() # 초기 데이터 생성
        header = Header(driver)
        home = HomePage(driver)
        signUpPage = SignUpPage(driver)
        articlePage = ArticlePage(driver)
        profilePage = ProfilePage(driver)

        try:
            # 테스트 환경 세팅
            header.click_sign_up_link()
            signUpPage.sign_up()

            # 테스트 시나리오 시작
            home.click_global_feed_tab_link()
            global_feed_first_article = articlePage.load_first_article_data()

            articlePage.click_preview_favorite(0, 1)

            header.click_my_profile_link()
            self.logger.info("My Profile 링크 클릭 완료")

            assert header.is_go_to_myprofile_page() # 기대 결과 1: 마이프로필로 진입되어야 함
            self.logger.info("마이프로필 페이지 이동 확인 완료")

            profilePage.click_favorited_article_tab_link()
            favorited_article_first_article = articlePage.load_first_article_data()

            assert all([ # 기대 결과 3: (좋아요 누른 Article 1개 이상) : 좋아요 누른 게시글이 노출됨
                global_feed_first_article["author"] == favorited_article_first_article["author"],
                global_feed_first_article["created date"] == favorited_article_first_article["created date"],
                global_feed_first_article["title"] == favorited_article_first_article["title"],
                global_feed_first_article["description"] == favorited_article_first_article["description"],
                global_feed_first_article["tags"] == favorited_article_first_article["tags"],
            ])

            articlePage.click_preview_favorite(0, 1)

            profilePage.click_my_article_tab_link()
            profilePage.click_favorited_article_tab_link()

            assert articlePage.is_empty_text_div_show() # 기대 결과 4: (좋아요 누른 Article X) : "No articles are here... yet." 텍스트가 노출됨

        except Exception as e:
            self.logger.error(f"❌ MYPROFILE_03 테스트 중 오류 발생: {e}")
            assert False

    def test_go_to_settings_from_profile(self, driver):
        """MYPROFILE_04: 마이프로필에서 '프로필 수정(Edit Profile Settings)' 버튼 클릭 시 설정 페이지로 이동 확인"""
        self.logger.info("마이 프로필에서 Edit Profile Settings 버튼 테스트 시작")
        header = Header(driver)
        signUpPage = SignUpPage(driver)
        profilePage = ProfilePage(driver)

        try:
            # 테스트 환경 세팅
            header.click_sign_up_link()
            signUpPage.sign_up()

            # 테스트 시나리오 시작
            header.click_my_profile_link()
            self.logger.info("My Profile 링크 클릭 완료")

            assert header.is_go_to_myprofile_page() # 기대 결과 1: 마이프로필로 진입되어야 함
            self.logger.info("마이프로필 페이지 이동 확인 완료")

            profilePage.click_edit_profile_settings_btn()
            self.logger.info("Edit Profile Settings 버튼 클릭 완료")

            assert header.is_go_to_settings_page() # 기대 결과 2: Settings 페이지로 진입되어야 함
            self.logger.info("설정 페이지 이동 확인 완료")

        except Exception as e:
            self.logger.error(f"❌ MYPROFILE_04 테스트 중 오류 발생: {e}")
            assert False