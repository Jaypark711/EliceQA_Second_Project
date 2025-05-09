from selenium.webdriver.common.by import By

from data.user_data import VALID_USER 
from pages.base_page import BasePage

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)