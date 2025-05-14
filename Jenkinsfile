pipeline {
    agent any

    environment {
        ENV_FILE = credentials('env-file')                // .env (qa/config/.env)
        USER_DATA_FILE = credentials('user-data-file')    // user_data.py (qa/data/user_data.py)
        DB_QUERIES_FILE = credentials('db-queries-file')  // db_queries.py (qa/db/db_queries.py)
    }

    stages {
        stage('Run Tests') {
            steps {
                sh '''
                    # 🔄 기존 파일 제거
                    rm -f qa/config/.env
                    rm -f qa/data/user_data.py
                    rm -f qa/db/db_queries.py

                    # 📦 Jenkins Credentials로부터 각 파일 복사
                    cp "$ENV_FILE" qa/config/.env
                    cp "$USER_DATA_FILE" qa/data/user_data.py
                    cp "$DB_QUERIES_FILE" qa/db/db_queries.py

                    # 🐍 가상환경 생성 및 테스트 실행
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
