import os
import subprocess
from dotenv import load_dotenv

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(dotenv_path=env_path)

JMETER_PATH = os.getenv("JMETER_PATH")

os.environ["JVM_ARGS"] = "-Djava.awt.headless=true"

def run_jmx(jmx_filename):
    """주어진 JMX 파일을 JMeter로 실행하고 HTML 리포트 생성"""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    jmx_path = os.path.join(project_root, 'performance', jmx_filename)
    result_path = os.path.join(project_root, 'reports', 'performance', f'{jmx_filename}_result.jtl')
    log_path = os.path.join(project_root, 'reports', 'performance', f'{jmx_filename}_log.log')
    html_path = os.path.join(project_root, 'reports', 'performance', f'{jmx_filename}_html')

    os.makedirs(os.path.dirname(result_path), exist_ok=True)

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
        cwd=os.path.dirname(jmx_path)
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