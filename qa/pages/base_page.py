from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver

from config.config import TIMEOUT

#디버깅용
import os
from datetime import datetime


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TIMEOUT)

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click_element(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        return element

    def send_keys(self, locator, text):
        element = self.click_element(locator)
        element.clear()
        element.send_keys(text)

    def get_attribute(self, locator, attribute):
        element = self.find_element(locator)
        return element.get_attribute(attribute)

    def get_text(self, locator):
        element = self.find_element(locator)
        return element.text

    def is_element_appear(self, locator):
        self.wait.until(EC.presence_of_element_located(locator))
        return True

    def is_element_disappear(self, locator):
        self.wait.until_not(EC.presence_of_element_located(locator))
        return True

    def is_element_active(self, locator):
        value = self.get_attribute(locator, "class")
        return "active" in value

    def wait_until_url_and_get(self, expected_url):
        self.wait.until(EC.url_to_be(expected_url))
        return self.driver.current_url
    
    #디버깅용


    def save_screenshot(self, name: str = "screenshot"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/{name}_{timestamp}.png"

        # 디렉토리 없으면 생성
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        self.driver.save_screenshot(filename)
        print(f"📸 스크린샷 저장 완료: {filename}")