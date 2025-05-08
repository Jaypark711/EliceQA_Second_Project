import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_experimental_option("excludeSwitches", ['enable-logging'])

    driver = webdriver.Chrome(options=options)
    
    yield driver

    driver.quit()