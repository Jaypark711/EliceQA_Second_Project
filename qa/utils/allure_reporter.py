import os
import shutil
import subprocess

def clean_allure_dirs():
    """allure-results와 allure-report 폴더를 제거"""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    results_dir = os.path.join(base_dir, 'reports', 'allure-results')
    report_dir = os.path.join(base_dir, 'reports', 'allure-report')

    for path in [results_dir, report_dir]:
        if os.path.exists(path):
            shutil.rmtree(path)

    os.makedirs(results_dir, exist_ok=True)

def generate_allure_report():
    """Allure 결과 파일을 기반으로 HTML 리포트를 생성(reports/allure-report)"""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    allure_results_dir = os.path.join(project_root, 'reports', 'allure-results')
    allure_report_dir = os.path.join(project_root, 'reports', 'allure-report')

    subprocess.run(
    ["/opt/allure/bin/allure", "generate", allure_results_dir, "-o", allure_report_dir, "--clean"],
        check=True
    )