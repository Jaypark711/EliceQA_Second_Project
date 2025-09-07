## 4️⃣ 엘리스 QA 트랙 1기 4팀 - 404 Not Found
- Open Soruce 프로젝트인 RealWorld 기반 Conduit 애플리케이션의 시나리오 기반 UI 테스트 자동화 프로젝트입니다.

## 👥 4팀 구성원
- **팀장** : 🍄 양송이
- **팀원** : 🐦 강연수, 🐻 박재윤  

## 🖥️ ️프로젝트 Repository 및 애플리케이션 정보
- **Backend** : https://github.com/gothinkster/node-express-realworld-example-app.git
- **Frontend** : https://github.com/gothinkster/react-redux-realworld-example-app.git
- **테스트 대상** : RealWorld 기반 Conduit 웹 사이트  

## 📌 프로젝트 개요
- Conduit은 RealWorld API 사양을 준수하는 실제 예제(CRUD, 인증, 고급 패턴)를 포함하는 코드 베이스 웹 사이트 프로젝트입니다.
![Conduit 스크린샷](https://blog.kakaocdn.net/dn/4mPCL/btsN2KOacQH/54da9Yxo5jrz4yY930QnKK/img.png)  

## 🌐 대상 서비스 주요 기능 (현재 프로젝트 기준)
#### 1. 게시글
- 마크다운 형식으로 본문 작성하여 게시글 본문 내 서식 적용 가능
- 주제 및 태그를 자유롭게 입력 및 지정하여 등록 가능
#### 2. 댓글
- 각 게시글에 댓글 작성 및 삭제 가능
#### 3. 소셜 기능
- 등록되어있는 게시글 중 마음에 드는 글 좋아요 등록 가능
- Conduit 내 회원의 프로필 방문 및 팔로우 기능
#### 4. 태그
- 각 게시물별로 태그 등록 가능
- 해당 태그와 관련된 게시물만 필터링하여 조회 가능
- Popular Tags게시글에 많이 등록된 상위 10개 항목 태그 확인 가능

## 🛠️ 사용 기술
- **테스트 자동화** : Python, Selenium, Pytest
- **API 테스트** : Postman, Newman
- **성능 테스트** : JMeter
- **CI** : Jenkins
- **버전 관리** : GitLab
- **테스트 환경** : Docker, Ubuntu 22.04.5 LTS

## ⌨️ 기능 / 페이지별 테스트 영역 담당
| 팀원     | 기능 / 페이지              |
|----------|----------------------------|
| 🍄 양송이 | Article                    |
| 🐦 강연수 | Auth, Filter, MyProfile    |
| 🐻 박재윤 | Comment, Social, Setting   |

## 🧑‍💻 팀원별 도구 및 기술 스택 담당
| 팀원     | 주요 도구 및 기술                                |
|----------|--------------------------------------------------|
| 🍄 양송이 | Allure, Postman, Newman                          |
| 🐦 강연수 | Allure, Postman, Newman, JMeter, Slack 연동      |
| 🐻 박재윤 | Allure, Docker, Jenkins                          |

## ⚙️ 환경 설정
#### 📁 `.env` 예시 (qa/config/.env)
```
DB_NAME = "your_db_name"
DB_USER = "your_db_user_id"
DB_PASSWORD = "your_password"
DB_HOST = "your_host_address_(ex.localhost)"
DB_PORT = "your_db_port"

RUNNER_NAME = "your_name"
SLACK_WEBHOOK_URL = "your_slack_webhook"
```  

#### 📁 `user_data.py` 예시 (qa/data/user_data.py)
```python
VALID_USER = {
    "username": "your_name",
    "email": "your_email",
    "password": "your_password"
}
```  

## 📂 디렉토리 구조
```
Project root/
├── backend/                                	# 테스트 환경에 포함된 Backend 애플리케이션 코드
├── frontend/                               	# 테스트 환경에 포함된 Frontend 애플리케이션 코드
├── qa/										# 자동화 테스트 코드의 Root 디렉토리
│   ├── api/
│   │   ├── collection.json					# api 테스트 컬렉션 파일
│   │   └── environment.json				    # api 테스트 환경 변수 파일
│   ├── components/							# 페이지를 구성하는 UI 컴포넌트 단위의 기능별 코드
│   │   └── header/
│   │   │   └── header_component.py
│   │   ├── body/
│   │   │   ├── article_component.py
│   │   │   ├── article_tab_component.py
│   │   │   ├── editor_component.py
│   │   │   ├── popular_tags_component.py
│   │   │   ├── profile_component.py
│   │   │   ├── settings_component.py
│   │   │   ├── sign_in_component.py
│   │   │   └── sign_up_component.py
│   │   └── footer/
│   ├── config/								# 환경 설정 파일 디렉토리
│   │   ├── .env
│   │   └── config.py
│   ├── data/								# 테스트 데이터 파일 디렉토리
│   │   ├── user_data.py
│   │   └── dummy_data.py
│   ├── db/                                 	# DB 관련 함수 디렉토리
│   │   ├── db_queries.py
│   │   └── db_utils.py
│   ├── pages/                              	# 페이지별 컴포넌트 조합 및 동작 정의 코드 디렉토리
│   │   ├── base_page.py
│   │   ├── editor_page.py
│   │   ├── home_page.py
│   │   ├── profile_page.py
│   │   ├── settings_page.py
│   │   ├── sign_in_page.py
│   │   └── sign_up_page.py
│   ├── performance/
│   │   ├── testdata/                       # 성능 테스트 Data 디렉토리
│   │   │   ├── article_data.csv
│   │   │   ├── signin_data.csv
│   │   │   └── signup_data.csv
│   │   ├── Article.jmx                     # 성능 테스트 jmx 파일
│   │   ├── Comment.jmx
│   │   ├── SignIn.jmx
│   │   └── SignUp.jmx
│   ├── reports/								# 테스트 결과 파일 디렉토리
│   ├── tests/								# 테스트 코드 파일 디렉토리
│   │   ├── conftest.py						# 테스트 환경 설정 파일
│   │   ├── test_article.py
│   │   ├── test_auth.py
│   │   ├── test_comment.py
│   │   ├── test_filter.py
│   │   ├── test_myprofile.py
│   │   ├── test_settings.py
│   │   └── test_social.py
│   └── utils/								# 테스트 유틸리티 함수 디렉토리
│       ├── allure_reporter.py				# allure 리포트 생성을 위한 유틸리티 파일
│       ├── api_runner.py					# api 테스트 실행 및 리포트 생성을 위한 유틸리티 파일
│       ├── performance_runner.py		    # 성능 테스트 실행 및 리포트 생성을 위한 유틸리티 파일
│       ├── helpers.py
│       ├── logger.py
│       └── slack_notifier.py				# 테스트 결과 Slack 전달을 위한 유틸리티 파일
├── requirements.txt							# python 의존성 패키지 목록 (pip install -r requirements.txt)
├── Jenkinsfile								# Jenkins CI/CD 파이프라인 정의 파일
├── Dockerfile.backend						# Backend 이미지 빌드를 위한 Dockerfile
├── Dockerfile.frontend						# Frontend 이미지 빌드를 위한 Dockerfile
├── docker-compose.yml						# 전체 서비스(docker) 실행 정의 파일
└── pytest.ini								# pytest 설정 파일 (테스트 옵션 지정)
```

## Test Case
링크 : 
```
https://docs.google.com/spreadsheets/d/1IggaI5biJJYo-Tz6klsjFcf8Zka6YXoz90u7UpSzidk/edit?usp=sharing
```
