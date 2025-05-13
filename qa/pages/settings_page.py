from pages.base_page import BasePage
from components.header.header_component import HeaderComponent
from components.body.settings_component import SettingsComponent

class SettingsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.header = HeaderComponent(driver)
        self.settings = SettingsComponent(driver)