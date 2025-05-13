from pages.base_page import BasePage
from components.header.header_component import HeaderComponent
from components.body.sign_up_component import SignUpComponent

class SignUpPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.header = HeaderComponent(driver)
        self.sign_up = SignUpComponent(driver)