// Jenkins CI/CD 파이프라인 정의 파일

pipeline {
    agent any
  
    stages {
        stage('Run Tests') {
            steps {
                sh '''
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
