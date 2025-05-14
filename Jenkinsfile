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
                    # 디렉토리 생성
                    mkdir -p qa/config
                    mkdir -p qa/data
                    mkdir -p qa/db

                    # 기존 파일 삭제
                    rm -f qa/config/.env
                    rm -f qa/data/user_data.py
                    rm -f qa/db/db_queries.py

                    # 파일 복사
                    cp "$ENV_FILE" qa/config/.env
                    cp "$USER_DATA_FILE" qa/data/user_data.py
                    cp "$DB_QUERIES_FILE" qa/db/db_queries.py

                    # 가상환경 설정 및 테스트 실행
                    python3 -m venv qa/venv
                    . qa/venv/bin/activate
                    pip install -r qa/requirements.txt

                    # 루트에서 qa 디렉토리 테스트 실행
                    python3 -m pytest qa
                '''
            }
        }
    }
}
