from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from config.config import BASE_URL, TIMEOUT

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TIMEOUT)

        driver.get(BASE_URL)

    # TODO: find/click/send_keys 등 동작별로 적절한 예외 분리 및 처리 메시지 세분화
    def find_element(self, locator):
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            return element
        
        except (NoSuchElementException, TimeoutException) as e:
            self.logger.error(f"{locator} 요소를 찾지 못하거나 대기 시간 초과: {e}")
            raise

    def find_elements(self, locator):
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(locator))
            return elements
        
        except (NoSuchElementException, TimeoutException) as e:
            self.logger.error(f"{locator} 요소를 찾지 못하거나 대기 시간 초과: {e}")
            raise

    def click_element(self, locator):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            return element
        
        except (NoSuchElementException, TimeoutException) as e:
            self.logger.error(f"{locator} 요소를 찾지 못하거나 대기 시간 초과: {e}")
            raise

    def send_keys(self, locator, text):
        try:
            element = self.click_element(locator)
            element.clear()
            element.send_keys(text)
        
        except (NoSuchElementException, TimeoutException) as e:
            self.logger.error(f"{locator} 요소를 찾지 못하거나 대기 시간 초과: {e}")
            raise

    def get_attribute(self, locator, attribute):
        try:
            element = self.find_element(locator)
            return element.get_attribute(attribute)
        
        except (NoSuchElementException, TimeoutException) as e:
            self.logger.error(f"{locator} 요소를 찾지 못하거나 대기 시간 초과: {e}")
            raise

    
    def get_text(self, locator):
        try:
            element = self.find_element(locator)
            return element.text
        
        except (NoSuchElementException, TimeoutException) as e:
            self.logger.error(f"{locator} 요소를 찾지 못하거나 대기 시간 초과: {e}")
            return False

    def is_element_disappear(self, locator):
        try:
            self.wait.until_not(EC.presence_of_element_located(locator))
            return True
        
        except (NoSuchElementException, TimeoutException) as e:
            self.logger.error(f"{locator} 요소를 찾지 못하거나 대기 시간 초과: {e}")
            return False
        
    def current_url(self):
        return self.driver.current_url