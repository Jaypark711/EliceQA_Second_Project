from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from config.config import BASE_URL
from utils.helpers import setupLogger

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = setupLogger(self.__class__.__name__)

        driver.get(BASE_URL)

    def find_element(self, locator):
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            return element
        
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
            element.send_keys(text)
        
        except (NoSuchElementException, TimeoutException) as e:
            self.logger.error(f"{locator} 요소를 찾지 못하거나 대기 시간 초과: {e}")
            raise