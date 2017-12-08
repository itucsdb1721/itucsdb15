import psycopg2 as dbapi2
from users import *
from flask import Flask

app = Flask(__name__)

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
            query = "DELETE FROM USERS WHERE (ID = %s)"
            cursor.execute(query, (key,))
            connection.commit()

    def update_user(conf, key, name, surname, nickname, email, password):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "UPDATE USERS SET NM = %s,SURNAME = %s, NICKNAME = %s, EMAIL = %s, PASSWORD = %s WHERE (ID = %d)"
            cursor.execute(query, (name, surname, nickname, email, password, key))
            connection.commit()

    def get_user(conf, username):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "SELECT NM, SURNAME, NICKNAME, EMAIL, PASSWORD FROM USERS WHERE NICKNAME = %s"
            cursor.execute(query, (username,))
            for row in cursor:
                (name, surname, nickname, email, password) = row
                return User(name, surname, nickname, email, password)

    def get_users(conf):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "SELECT ID, NM, SURNAME, NICKNAME, EMAIL, PASSWORD FROM USERS ORDER BY ID"
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


