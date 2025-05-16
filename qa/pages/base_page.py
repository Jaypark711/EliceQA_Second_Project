from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver

from config.config import TIMEOUT

class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TIMEOUT)

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click_element(self, locator):
        self.wait.until(EC.presence_of_element_located(locator))
        self.wait.until(EC.visibility_of_element_located(locator))
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