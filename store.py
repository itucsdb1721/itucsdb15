import psycopg2 as dbapi2
from users import *

class Store:
    def add_user(conf, users):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query2 = """INSERT INTO USERS (NM, SURNAME, NICKNAME, EMAIL, PASSWORD ) VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query2, (users.name, users.surname, users.nickname, users.email, users.password))
            connection.commit()

    def delete_user(conf, key):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM USERS WHERE (USER_ID = %s)"
            cursor.execute(query, (key,))
            connection.commit()

    def update_password(conf, username, new_password):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "UPDATE USERS SET PASSWORD = %s WHERE (NICKNAME = %s)"
            cursor.execute(query, (new_password, username))
            connection.commit()

    def get_user(conf, username):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "SELECT NM, SURNAME, NICKNAME, EMAIL, PASSWORD FROM USERS WHERE NICKNAME = %s"
            cursor.execute(query, (username,))
            for row in cursor:
                (name, surname, nickname, email, password) = row
                return User(name, surname, nickname, email, password)

    def get_userid(conf, username):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "SELECT USER_ID FROM USERS WHERE NICKNAME = %s"
            cursor.execute(query, (username,))
            for row in cursor:
                user_id = row
                return user_id

    def get_users(conf):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "SELECT USER_ID, NM, SURNAME, NICKNAME, EMAIL, PASSWORD FROM USERS ORDER BY USER_ID"
            cursor.execute(query)
            users = [(key, User(name, surname, nickname, email, password))
                      for key, name, surname, nickname, email, password in cursor]
        return users

    def is_exist(conf, username):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "SELECT PASSWORD FROM USERS WHERE NICKNAME = %s"
            cursor.execute(query, (username,))
            for row in cursor:
                (hashed,) = row
                return hashed


