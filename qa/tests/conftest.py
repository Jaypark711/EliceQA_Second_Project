# conftest.py

import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from utils.allure_reporter import clean_allure_dirs, generate_allure_report
from utils.slack_notifier import send_test_result_to_slack

def pytest_sessionstart(session):
    print("\n🚀 pytest_sessionstart: Allure 디렉토리 초기화 중")
    clean_allure_dirs()

def pytest_sessionfinish(session, exitstatus):
    print("\n✅ pytest_sessionfinish: 리포트 생성 및 Slack 전송 중")
    generate_allure_report()
    send_test_result_to_slack()

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_experimental_option("excludeSwitches", ['enable-logging'])

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    yield driver

    driver.quit()