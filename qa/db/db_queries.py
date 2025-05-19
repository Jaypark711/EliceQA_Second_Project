# User 관련
SQL_INSERT_USER = """
    INSERT INTO "User" (email, username, password, image, bio, demo)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING id;
"""
SQL_DELETE_ALL_USER = 'DELETE FROM public."User";'
SQL_GET_USER_INFO_BY_USERNAME = """
    SELECT username, image, bio
    FROM public."User"
    WHERE username = %s;
"""
SQL_GET_USER_ID_BY_USERNAME = 'SELECT id FROM public."User" WHERE username = %s'

# Tag 관련
SQL_INSERT_TAG = """
    INSERT INTO "Tag" (name)
    VALUES (%s)
    RETURNING id;
"""
SQL_DELETE_ALL_TAG = 'DELETE FROM public."Tag";'
SQL_GET_ARTICLE_COUNT_BY_NAME = """
    SELECT COUNT(*) 
    FROM public."_ArticleToTag" AS article_tag
    JOIN public."Tag" AS tag ON article_tag."B" = tag.id
    WHERE tag.name = %s;
"""

# Article 관련
SQL_INSERT_ARTICLE = """
    INSERT INTO "Article" ("slug", "title", "description", "body", "createdAt", "updatedAt", "authorId")
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    RETURNING id;
"""
SQL_GET_ARTICLES_BY_TITLE = 'SELECT * FROM public."Article" WHERE title = %s'
SQL_GET_ARTICLE_DETAILS_BY_SLUG = 'SELECT * FROM public."Article" WHERE "slug" = %s'
SQL_GET_FAVORITED_ARTICLE_TITLE_BY_USERNAME =  """
    SELECT a.title
    FROM public."Article" a
    JOIN public."_UserFavorites" uf ON a."id" = uf."A"
    JOIN public."User" u ON uf."B" = u."id"
    WHERE u.username = %s;
"""

# _ArticleToTag 관련
SQL_INSERT_ARTICLE_TAG = """
    INSERT INTO "_ArticleToTag" ("A", "B")
    VALUES (%s, %s)
    ON CONFLICT DO NOTHING;
"""