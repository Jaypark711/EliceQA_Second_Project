import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from db.db_utils import init_db
from utils.allure_reporter import clean_allure_dirs, generate_allure_report
from utils.slack_notifier import send_pytest_result_to_slack, send_newman_result_to_slack, send_jmeter_result_to_slack
from utils.api_runner import run_newman
from utils.performance_runner import run_jmeter

def pytest_sessionstart(session):
    print("\n🚀 pytest_sessionstart")

    clean_allure_dirs()
    print("✅ Allure 디렉토리 초기화 완료")

def pytest_sessionfinish(session, exitstatus):
    print("\n🚀 pytest_sessionfinish")

    init_db()
    print("✅ DB 초기화 완료")

    generate_allure_report()
    print("✅ Allure Report 생성 완료")

    send_pytest_result_to_slack()
    print("✅ UI Test Result를 Slack에 전송 완료")

    run_newman()
    print("✅ newman 실행 및 Report 생성 완료")

    send_newman_result_to_slack()
    print("✅ API Test Result를 Slack에 전송 완료")    
    
    init_db()
    print("✅ DB 초기화 완료")

    run_jmeter()
    print("✅ jmeter 실행 및 Report 생성 완료")

    send_jmeter_result_to_slack(["SignUp.jmx", "SignIn.jmx", "Article.jmx", "Comment.jmx"])
    print("✅ Performance Test Result를 Slack에 전송 완료")

@pytest.fixture(scope='function')
def driver():
    options = Options()
    options.add_argument("--lang=ko")
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument("--headless=new")
    options.add_experimental_option("prefs", {
        "intl.accept_languages": "ko-KR,ko"
    })
    options.add_experimental_option("excludeSwitches", ['enable-logging'])

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    yield driver

    driver.quit()