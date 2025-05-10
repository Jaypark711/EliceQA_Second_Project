from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from config.config import BASE_URL, TIMEOUT

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TIMEOUT)

        driver.get(BASE_URL)

    def find_element(self, locator):
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            return element
        
        except Exception as e:
            self.logger.error(f"{locator} 요소를 찾는 중 오류 발생: {e}")
            raise

    def find_elements(self, locator):
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(locator))
            return elements
        
        except Exception as e:
            self.logger.error(f"{locator} 요소들을 찾는 중 오류 발생: {e}")
            raise

    def click_element(self, locator):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            return element
        
        except Exception as e:
            self.logger.error(f"{locator} 요소를 클릭하는 중 오류 발생: {e}")
            raise

    def send_keys(self, locator, text):
        try:
            element = self.click_element(locator)
            element.clear()
            element.send_keys(text)
        
        except Exception as e:
            self.logger.error(f"{locator} 요소에 {text} 값을 입력하는 중 오류 발생: {e}")
            raise

    def get_attribute(self, locator, attribute):
        try:
            element = self.find_element(locator)
            return element.get_attribute(attribute)
        
        except Exception as e:
            self.logger.error(f"{locator} 요소에서 {attribute} 속성 값을 가져오는 중 오류 발생: {e}")
            raise

    def get_text(self, locator):
        try:
            element = self.find_element(locator)
            return element.text
        
        except Exception as e:
            self.logger.error(f"{locator} 요소의 텍스트를 가져오는 중 오류 발생: {e}")
            raise

    def is_element_disappear(self, locator):
        try:
            self.wait.until_not(EC.presence_of_element_located(locator))
            return True
        
        except Exception as e:
            self.logger.error(f"{locator} 요소가 사라질때까지 대기하는 중 오류 발생: {e}")
            raise

    def is_element_active(self, locator):
        try:
            value = self.get_attribute(locator, "class")
            return "active" in value
        except Exception as e:
            self.logger.error(f"{locator} 요소의 class 속성에서 'active' 포함 여부 확인 중 오류 발생: {e}")
            raise
        
    def get_current_url(self):
        try:
            url = self.driver.current_url
            return url
        except Exception as e:
            self.logger.error(f"현재 URL을 가져오는 중 오류 발생: {e}")
            raise