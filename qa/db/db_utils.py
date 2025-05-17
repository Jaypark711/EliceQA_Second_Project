import os
import psycopg2
import subprocess
from dotenv import load_dotenv
from datetime import datetime
from faker import Faker
from db import db_queries
import random
faker = Faker()

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

# def run_prisma_seed():
#     """backend 디렉토리 기준으로 Prisma seed 명령어 실행 (초기 데이터 입력용)"""
#     backend_dir = os.path.join(os.getenv('WORKSPACE'), 'backend')
#     subprocess.run(
#         ["npx", "prisma", "db", "seed"],
#         cwd=backend_dir,
#         shell=True,
#         check=True
#     )

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

def seed_users(count=12):
    """Faker를 이용해 사용자 더미 데이터를 생성하고 DB에 삽입"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        for _ in range(count):
            email = faker.unique.email()
            username = faker.unique.user_name()
            password = faker.password()
            image = "https://api.realworld.io/images/demo-avatar.png"
            cur.execute("""
                INSERT INTO "User" (email, username, password, image)
                VALUES (%s, %s, %s, %s);
            """, (email, username, password, image))
        conn.commit()
        print(f"✅ 사용자 {count}명 삽입 완료")
    except Exception as e:
        conn.rollback()
        print(f"❌ 사용자 삽입 실패: {e}")
    finally:
        cur.close()
        conn.close()

def seed_articles(count=6):
    """Faker를 이용해 기사 더미 데이터를 생성하고 DB에 삽입"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT id FROM "User";')
        user_ids = [row[0] for row in cur.fetchall()]
        for _ in range(count):
            title = faker.sentence(nb_words=6)
            slug = "-".join(title.lower().split())
            description = faker.paragraph()
            body = faker.text(max_nb_chars=800)
            now = datetime.now()
            author_id = random.choice(user_ids)
            cur.execute("""
                INSERT INTO "Article" (slug, title, description, body, "createdAt", "updatedAt", "authorId")
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (slug, title, description, body, now, now, author_id))
        conn.commit()
        print(f"✅ 기사 {count}개 삽입 완료")
    except Exception as e:
        conn.rollback()
        print(f"❌ 기사 삽입 실패: {e}")
    finally:
        cur.close()
        conn.close()

def seed_tags(count=23):
    """Faker를 이용해 태그 더미 데이터를 생성하고 DB에 삽입"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        for _ in range(count):
            name = faker.unique.word()
            cur.execute('INSERT INTO "Tag" (name) VALUES (%s);', (name,))
        conn.commit()
        print(f"✅ 태그 {count}개 삽입 완료")
    except Exception as e:
        conn.rollback()
        print(f"❌ 태그 삽입 실패: {e}")
    finally:
        cur.close()
        conn.close()

def seed_article_to_tag(count=23):
    """기사와 태그를 무작위로 연결하여 관계 테이블에 삽입"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT id FROM "Article";')
        article_ids = [row[0] for row in cur.fetchall()]
        cur.execute('SELECT id FROM "Tag";')
        tag_ids = [row[0] for row in cur.fetchall()]
        used = set()
        while len(used) < count:
            a = random.choice(article_ids)
            t = random.choice(tag_ids)
            if (a, t) not in used:
                cur.execute('INSERT INTO "_ArticleToTag" (article_id, tag_id) VALUES (%s, %s);', (a, t))
                used.add((a, t))
        conn.commit()
        print(f"✅ 기사-태그 관계 {count}개 삽입 완료")
    except Exception as e:
        conn.rollback()
        print(f"❌ 관계 삽입 실패: {e}")
    finally:
        cur.close()
        conn.close()

def run_prisma_seed():
    seed_users()
    seed_articles()
    seed_tags()
    seed_article_to_tag()
