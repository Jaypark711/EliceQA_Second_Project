import os
import subprocess
from dotenv import load_dotenv

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(dotenv_path=env_path)

JMETER_PATH = os.getenv("JMETER_PATH")

# GUI 없는 환경에서도 실행되도록 JVM 설정
os.environ["JVM_ARGS"] = "-Djava.awt.headless=true"

# 실행 경로(CSV 참조 기준)를 JMX가 있는 디렉토리로 지정
JMX_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'performance'))

def run_jmx(jmx_filename):
    """주어진 JMX 파일을 JMeter로 실행하고 HTML 리포트 생성"""
    report_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'reports', 'performance'))
    jmx_path = os.path.join(JMX_DIR, jmx_filename)
    result_path = os.path.join(report_dir, f'{jmx_filename}_result.jtl')
    log_path = os.path.join(report_dir, f'{jmx_filename}_log.log')
    html_path = os.path.join(report_dir, f'{jmx_filename}_html')

    os.makedirs(report_dir, exist_ok=True)

    # 1️⃣ JMeter 테스트 실행 (.jtl, .log 생성)
    subprocess.run(
        [
            JMETER_PATH,
            "-n", "-t", jmx_path,
            "-l", result_path,
            "-j", log_path
        ],
        check=True,
        shell=True,
        cwd=JMX_DIR 
    )

    # 2️⃣ HTML 리포트 생성
    subprocess.run(
        [
            JMETER_PATH,
            "-g", result_path,
            "-o", html_path
        ],
        check=True,
        shell=True
    )

    print(f"✅ {jmx_filename} 실행 완료 / HTML 리포트 생성됨: {html_path}/index.html")

def run_jmeter():
    run_jmx("SignUp.jmx")
    run_jmx("SignIn.jmx")
    run_jmx("Article.jmx")
    run_jmx("Comment.jmx")