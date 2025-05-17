import os
import random
import psycopg2
from faker import Faker
from datetime import datetime
from dotenv import load_dotenv

from db import db_queries

def get_connection():
    """.env 파일에서 DB 연결 정보를 로드하고 PostgreSQL 커넥션 객체 반환"""
    load_dotenv(dotenv_path='config/.env')
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

    return conn

def init_db():
    """User 테이블 및 Tag 테이블의 모든 레코드 삭제"""
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute(db_queries.SQL_DELETE_ALL_USER)
    cur.execute(db_queries.SQL_DELETE_ALL_TAG)
    conn.commit()

    cur.close()
    conn.close()

def run_prisma_seed():
    conn = get_connection()
    cur = conn.cursor()

    faker = Faker()

    """1. Tag 20 ~ 30개 생성"""
    tag_ids = []
    for i in range(random.randint(20, 30)):
        tag_name = f"tag_{i}"
        cur.execute(db_queries.SQL_INSERT_TAG, (tag_name,))
        tag_id = cur.fetchone()[0]
        tag_ids.append(tag_id)

    """2. User 1 ~ 3명 생성"""
    user_ids = []
    for _ in range(random.randint(1, 3)):
        email = faker.email()
        username = faker.user_name()
        password = faker.password()
        image = "https://api.realworld.io/images/smiley-cyrus.jpeg"
        bio = faker.sentence()
        cur.execute(db_queries.SQL_INSERT_USER, (email, username, password, image, bio, True))
        user_id = cur.fetchone()[0]
        user_ids.append(user_id)

        """3.User 당 Article 1~3개 생성"""
        for _ in range(random.randint(1, 3)):
            slug = faker.slug()
            title = faker.sentence()
            description = faker.sentence()
            body = faker.paragraph()
            now = datetime.now()

            cur.execute(db_queries.SQL_INSERT_ARTICLE, (slug, title, description, body, now, now, user_id))
            article_id = cur.fetchone()[0]

            """4. ArticleToTag 연결 2 ~ 4개"""
            linked_tag_ids = random.sample(tag_ids, k=random.randint(2, 4))
            for tag_id in linked_tag_ids:
                cur.execute(db_queries.SQL_INSERT_ARTICLE_TAG, (article_id, tag_id))

    conn.commit()
    
    cur.close()
    conn.close()

def get_article_count_by_tag_name(tag_name):
    """특정 태그 이름(tag_name)을 가진 게시글의 수를 반환 (_ArticleToTag 테이블과 Tag 테이블을 조인하여 카운트)"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(db_queries.SQL_GET_ARTICLE_COUNT_BY_NAME, (tag_name,))

    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return count

def get_user_info_by_username(username):
    """특정 사용자명(username)에 해당하는 유저의 유저명, 프로필 이미지, 소개를 튜플로 반환"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(db_queries.SQL_GET_USER_INFO_BY_USERNAME, (username,))

    result = cur.fetchone()

    cur.close()
    conn.close()
    
    return result

def get_favorited_article_title_by_username(username):
    """username을 기준으로 좋아요 누른 가장 최근 게시글의 title 반환 """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(db_queries.SQL_GET_FAVORITED_ARTICLE_TITLE_BY_USERNAME, (username,))

    result = cur.fetchone()[0]

    cur.close()
    conn.close()

    return result

def get_user_id_by_username(username):
    """특정 사용자명(username)에 해당하는 유저의 id 번호 값을 튜플로 받아 가져오기"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(db_queries.SQL_GET_USER_ID_BY_USERNAME, (username,))

    result = cur.fetchone()[0]

    return result

def get_articles_by_title(title):
    """ 타이틀명(title)으로 article을 찾아 실제로 게시글이 DB에 존재하는지 확인하기"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(db_queries.SQL_GET_ARTICLES_BY_TITLE, (title,))

    result = cur.fetchone()

    cur.close()
    conn.close()
    
    return result

def get_article_details_by_slug(slug):
    """ slug로 글 정보 불러오기 """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(db_queries.SQL_GET_ARTICLE_DETAILS_BY_SLUG, (slug,))

    result = cur.fetchone()

    cur.close()
    conn.close()

    return result