import pytest

from config.config import BASE_URL, VALID_USER
from pages.header.header import Header
from pages.body.signup_page import SignUpPage
from pages.body.profile_page import ProfilePage
from pages.body.article_page import ArticlePage
from utils.logger import setupLogger
from db.db_utils import delete_all_user, get_user_info_by_username

@pytest.mark.usefixtures("driver")
class TestMyProfile:
    logger = setupLogger(__qualname__)

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, driver):
        delete_all_user() # 테스트 환경 초기화: 상태 의존성을 제거하고 동일한 초기 조건 보장
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

    # @pytest.mark.parametrize("title, description, body, tags", [
    #     ("제목", "설명", "내용", ["태그"])
    # ])
    # def test_show_my_articles(self, driver, title, description, body, tags):
    #     """MYPROFILE_02: 마이프로필에서 내가 작성한 게시글 목록(My Articles) 표시 확인"""
    #     self.logger.info("마이프로필에서 My Articles 탭 테스트 시작")
    #     header = Header(driver)
    #     signUpPage = SignUpPage(driver)
    #     profilePage = ProfilePage(driver)
    #     articlePage = ArticlePage(driver)

    #     try:
    #         # 테스트 환경 세팅
    #         header.click_sign_up_link()
    #         signUpPage.sign_up()

    #         # 테스트 시나리오 시작
    #         header.click_my_profile_link()
    #         profilePage.click_my_article_tab_link()
    #         assert all([ # 기대 결과 1: 마이프로필로 진입되어야 하며, My Articles 탭이 자동 선택됨
    #             header.is_go_to_myprofile_page(),
    #             profilePage.is_my_article_tab_active()
    #         ])
    #         self.logger.info("마이 프로필에서 My Articles 탭 클릭 및 탭 활성화 확인")

    #         assert profilePage.is_empty_text_div_show() # 기대 결과 2: (등록된 Article X) : "No articles are here... yet." 텍스트가 노출됨
    #         self.logger.info("등록된 Article이 없는 경우 'No articles are here... yet.' 텍스트 노출 확인")

    #         header.click_new_post_link()
    #         articlePage.save_article(title, description, body, tags)

    #         header.click_my_profile_link()
    #         articles = articlePage.load_article_preview_lists()

    #         assert all([ # 기대 결과 3: (등록 Article 1개 이상) : 내가 작성한 게시글 목록이 표시되어야 함
    #             articles["article1"]["title"] == title,
    #             articles["article1"]["description"] == description,
    #             articles["article1"]["tags"] == tags[0],
    #         ])
    #         self.logger.info("등록된 Article이 있는 경우 내가 작성한 게시글 목록 표시 확인")

    #     except Exception as e:
    #         self.logger.error(f"❌ MYPROFILE_02 테스트 중 오류 발생: {e}")
    #         assert False

    # def test_show_favorited_articles(self, driver):
    #     """MYPROFILE_03: 마이프로필에서 좋아요 누른 게시글 목록(Favorited Articles) 표시 확인"""
    #     self.logger.info("마이프로필에서 Favorited Articles 탭 테스트 시작")
    #     header = Header(driver)
    #     signInPage = SignInPage(driver)
    #     profilePage = ProfilePage(driver)

    #     header.click_sign_in_link()
    #     signInPage.login()
    #     self.logger.info("로그인 성공")

    #     header.click_my_profile_link()
    #     profilePage.click_favorited_article_tab_link()
    #     assert profilePage.is_favorited_article_tab_active() == True
    #     self.logger.info("마이 프로필에서 Favorited Articles 탭 클릭 및 탭 활성화 확인")

    #     # TODO: 내가 즐겨찾기한 게시글만 보이는지 확인 (게시글 정보 불러오는 함수 구현 전까지 대기)

    # def test_go_to_settings_from_profile(self, driver):
    #     """MYPROFILE_04: 마이프로필에서 '프로필 수정(Edit Profile Settings)' 버튼 클릭 시 설정 페이지로 이동 확인"""
    #     self.logger.info("마이 프로필에서 Edit Profile Settings 버튼 테스트 시작")
    #     header = Header(driver)
    #     signUpPage = SignUpPage(driver)
    #     profilePage = ProfilePage(driver)

    #     try:
    #         # 테스트 환경 세팅
    #         header.click_sign_up_link()
    #         signUpPage.sign_up()

    #         # 테스트 시나리오 시작
    #         header.click_my_profile_link()
    #         self.logger.info("My Profile 링크 클릭 완료")

    #         assert header.is_go_to_myprofile_page() # 기대 결과 1: 마이프로필로 진입되어야 함
    #         self.logger.info("마이프로필 페이지 이동 확인 완료")

    #         profilePage.click_edit_profile_settings_btn()
    #         self.logger.info("Edit Profile Settings 버튼 클릭 완료")

    #         assert header.is_go_to_settings_page() # 기대 결과 2: Settings 페이지로 진입되어야 함
    #         self.logger.info("설정 페이지 이동 확인 완료")

    #     except Exception as e:
    #         self.logger.error(f"❌ MYPROFILE_04 테스트 중 오류 발생: {e}")
    #         assert False