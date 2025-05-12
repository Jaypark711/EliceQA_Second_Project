import os
import psycopg2
import subprocess
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
    """User 테이블의 모든 레코드 삭제"""
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute(db_queries.SQL_DELETE_ALL_USER)
    cur.execute(db_queries.SQL_DELETE_ALL_TAG)
    conn.commit()

    cur.close()
    conn.close()

def run_prisma_seed():
    """backend 디렉토리 기준으로 Prisma seed 명령어 실행 (초기 데이터 입력용)"""
    backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

    subprocess.run(
        ["npx", "prisma", "db", "seed"],
        cwd=backend_dir,
        shell=True,
        check=True
    )

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

def get_title_where_favorite(username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(db_queries.SQL_GET_TITLE_WHERE_FAVORITE, (username,))
    result = cur.fetchone()[0]
    cur.close()
    conn.close()
    return result