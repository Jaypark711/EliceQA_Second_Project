from pages.base_page import BasePage
from components.header.header_component import HeaderComponent
from components.body.editor_component import EditorComponent

class EditorPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.header = HeaderComponent(driver)
        self.editor = EditorComponent(driver)