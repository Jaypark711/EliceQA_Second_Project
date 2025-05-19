pipeline {
    agent any

    environment {
        ENV_FILE        = credentials('env-file')
        USER_DATA_FILE  = credentials('user-data-file')
    }

    stages {
        stage('Run Tests') {
            steps {
                sh '''
                    mkdir -p qa/config qa/data
                    # 디렉토리 초기화
                    rm -rf qa/config/.env
                    rm -rf qa/data/user_data.py

                    # 파일 복사
                    cp "$ENV_FILE" qa/config/.env
                    cp "$USER_DATA_FILE" qa/data/user_data.py

                    # 가상환경 설정 및 QA 디렉토리에서 테스트 실행
                    cd qa
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    python3 -m pytest tests/test_comment.py
                '''
            }
        }
    }
}
