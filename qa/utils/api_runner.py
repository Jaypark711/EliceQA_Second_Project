import os
import subprocess

def run_newman():
    """htmlextra 리포터를 사용하여 Newman으로 Postman 테스트 실행"""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    collection_path = os.path.join(project_root, 'api', 'collection.json')
    env_path = os.path.join(project_root, 'api', 'environment.json')
    report_path = os.path.join(project_root, 'reports', 'postman_report.html')

    subprocess.run(
        [
            "newman", "run", collection_path,
            "-e", env_path,
            "-r", "htmlextra",
            "--reporter-htmlextra-export", report_path
        ],
        check=True,
        shell=True
    )