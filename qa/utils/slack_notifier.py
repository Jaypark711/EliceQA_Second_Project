import os
import json
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path='config/.env')

runner_name = os.getenv("RUNNER_NAME")
slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")

def send_pytest_result_to_slack():
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

    if failed_tests:
        failed_summary = "\n".join([f"• {name}" for name in failed_tests])
    else:
        failed_summary = "없음"

    message = {
        "text": f"""
        📢 *UI 자동화 테스트 결과 (by {runner_name})*
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

def send_newman_result_to_slack():
    json_path = "reports/postman_report.json"

    if not os.path.exists(json_path):
        print("❌ Newman 결과 파일이 존재하지 않습니다.")
        return

    try:
        with open(json_path, encoding="utf-8") as f:
            result = json.load(f)

        stats = result["run"]["stats"]

        # 항목별 통계
        requests_total = stats["requests"]["total"]
        requests_failed = stats["requests"]["failed"]

        prereq_total = stats["prerequestScripts"]["total"]
        prereq_failed = stats["prerequestScripts"]["failed"]

        test_scripts_total = stats["testScripts"]["total"]
        test_scripts_failed = stats["testScripts"]["failed"]

        assertions_total = stats["assertions"]["total"]
        assertions_failed = stats["assertions"]["failed"]

        skipped_tests = stats.get("skippedTests", {}).get("total", 0)

        # 실패한 테스트 목록 수집
        failures = result["run"].get("failures", [])
        failed_tests = [
            f"{f['source']['name']} - {f['error']['message']}" for f in failures
        ]
        failed_summary = "\n".join([f"• {name}" for name in failed_tests]) if failed_tests else "없음"

        # Slack 메시지 구성
        message = {
            "text": f"""
            📢 *API 자동화 테스트 결과 (by {runner_name})*
        • Requests:
         ✅ Passed: {requests_total - requests_failed}
         ❌ Failed: {requests_failed}
        • Prerequest Scripts:
         ✅ Passed: {prereq_total - prereq_failed} 
         ❌ Failed: {prereq_failed}
        • Test Scripts: 
         ✅ Passed: {test_scripts_total - test_scripts_failed}  
         ❌ Failed: {test_scripts_failed}
        • Assertions: 
         ✅ Passed: {assertions_total - assertions_failed} 
         ❌ Failed: {assertions_failed}
        • Skipped Tests: 
         ⏭️ Skipped: {skipped_tests}

        🧪 *실패한 테스트 목록:*
        {failed_summary}
        """
        }

        response = requests.post(slack_webhook_url, json=message)
        print(f"Slack 응답 코드: {response.status_code}")

    except Exception as e:
        print(f"❌ Newman 결과 파싱 실패: {e}")