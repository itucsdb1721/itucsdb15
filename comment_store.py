import psycopg2 as dbapi2
from comment import Comment

class CommentStore:
    def add_comment(conf, comments):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query2 = """INSERT INTO COMMENTS (USER_ID, PRODUCT_ID, COMMENT) VALUES (%s, %s, %s)"""
            cursor.execute(query2, (comments.user_id, comments.product_id, comments.comment))
            connection.commit()

    def delete_comment(conf, key):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM COMMENTS WHERE (COMMENT_ID = %s)"
            cursor.execute(query, (key,))
            connection.commit()

    def update_comment(conf, comment_id, newcomment):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "UPDATE COMMENTS SET COMMENT = %s WHERE (COMMENT_ID = %s)"
            cursor.execute(query, (newcomment, comment_id))
            connection.commit()

    def get_comment_for_product(conf, product_id):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "SELECT NICKNAME, COMMENT, COMMENT_ID FROM COMMENTS INNER JOIN USERS ON COMMENTS.USER_ID = USERS.USER_ID WHERE PRODUCT_ID = %s ORDER BY COMMENT_ID DESC"
            cursor.execute(query, (product_id,))
            comments = cursor.fetchall()
            return comments

    def get_commentid(conf, username):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "SELECT COMMENT_ID FROM COMMENTS WHERE USER_ID = %s AND PRODUCT_ID = %s AND COMMENT = %s"
            cursor.execute(query, (username,))
            for row in cursor:
                comment_id = row
                return comment_id

    def get_users(conf):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "SELECT COMMENT_ID, USER_ID, COMMENT FROM COMMENTS ORDER BY COMMENT_ID DESC"
            cursor.execute(query)
            users = [(key, Comment(user_id, product_id, comment))
                      for key, user_id, product_id, comment in cursor]
        return users
