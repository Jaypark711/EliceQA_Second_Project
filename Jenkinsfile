pipeline {
    agent any

    environment {
        ENV_FILE        = credentials('env-file')
        USER_DATA_FILE  = credentials('user-data-file')
        DB_QUERIES_FILE = credentials('db-queries-file')
    }

    stages {
        stage('Run Tests') {
            steps {
                sh '''
                    mkdir -p qa/config qa/data qa/db
                    # 디렉토리 초기화
                    rm -rf qa/config/.env
                    rm -rf qa/data/user_data.py
                    rm -rf qa/db/db_queries.py

                    # 파일 복사
                    cp "$ENV_FILE" qa/config/.env
                    cp "$USER_DATA_FILE" qa/data/user_data.py
                    cp "$DB_QUERIES_FILE" qa/db/db_queries.py

                    # 가상환경 설정 및 QA 디렉토리에서 테스트 실행
                    cd qa
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    python3 -m pytest 
                '''
            }
        }
    }
}
