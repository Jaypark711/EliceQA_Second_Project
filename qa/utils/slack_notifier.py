import os
import json
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path='qa/config/.env')
runner_name = os.getenv("RUNNER_NAME")
slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")

def send_test_result_to_slack():
    try:
        summary_path = "reports/allure-report/widgets/summary.json"
        with open(summary_path, encoding="utf-8") as f:
            data = json.load(f)
            stats = data["statistic"]
            passed = stats["passed"]
            failed = stats["failed"]
            skipped = stats["skipped"]
            total = stats["total"]
    except Exception as e:
        print(f"요약 정보 파싱 실패: {e}")
        passed = failed = skipped = total = "N/A"

    # 🔍 실패한 테스트 목록 수집
    failed_tests = []
    results_dir = "reports/allure-results"
    if os.path.exists(results_dir):
        for file in os.listdir(results_dir):
            if file.endswith("-result.json"):
                file_path = os.path.join(results_dir, file)
                try:
                    with open(file_path, encoding="utf-8") as f:
                        result_data = json.load(f)
                        if result_data.get("status") == "failed":
                            test_name = result_data.get("fullName") or result_data.get("name")
                            failed_tests.append(test_name)
                except Exception as e:
                    print(f"결과 파일 파싱 오류: {file} → {e}")

    # 🔹 실패 테스트 출력 정리
    if failed_tests:
        failed_summary = "\n".join([f"• {name}" for name in failed_tests])
    else:
        failed_summary = "없음"

    # 📤 Slack 메시지 구성
    message = {
        "text": f"""
        📢 *자동화 테스트 결과 (by {runner_name})*
        ✅ Passed: {passed}
        ❌ Failed: {failed}
        ⏭️ Skipped: {skipped}
        📊 Total: {total}

        🧪 *실패한 테스트 목록:*
        {failed_summary}
        """
    }

    response = requests.post(slack_webhook_url, json=message)
    print(f"Slack 응답 코드: {response.status_code}")