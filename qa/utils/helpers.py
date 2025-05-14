from config.config import TIMEOUT
from selenium.webdriver.support.ui import WebDriverWait

class Helpers:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, TIMEOUT)

    # 페이지 로드가 완료될 때 까지 대기
    def wait_until_page_load_complete(self):
        self.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )