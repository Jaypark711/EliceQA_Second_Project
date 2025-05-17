import os
import subprocess

def run_newman():
    """htmlextra + json 리포터를 사용하여 Newman으로 Postman 테스트 실행 및 리포트 저장"""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    collection_path = os.path.join(project_root, 'api', 'collection.json')
    env_path = os.path.join(project_root, 'api', 'environment.json')
    html_report_path = os.path.join(project_root, 'reports', 'postman_report.html')
    json_report_path = os.path.join(project_root, 'reports', 'postman_report.json')

    result = subprocess.run(
        [
            "/usr/local/bin/newman", "run", collection_path,
            "-e", env_path,
            "-r", "htmlextra,json",
            "--reporter-htmlextra-export", html_report_path,
            "--reporter-json-export", json_report_path
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    print("📤 Newman stdout:\n", result.stdout)
    print("🛑 Newman stderr:\n", result.stderr)

    if result.returncode != 0:
        raise RuntimeError(f"Newman failed with exit code {result.returncode}")