import psycopg2 as dbapi2
from products import Product, Clothes

class ClotheStore:
    def add_clothe(conf, product, clothes):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query2 = """INSERT INTO PRODUCTS (PNAME, PIC, PKIND, PRICE, USER_ID) VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query2, (product.name, product.pic_link, product.kind, product.price, product.seller))

            query2 = """SELECT PRODUCT_ID FROM PRODUCTS WHERE PNAME = %s AND PKIND = %s AND PRICE = %s AND USER_ID = %s"""
            cursor.execute(query2, (product.name, product.kind, product.price, product.seller))

            for row in cursor:
                product_id = row

            query2 = """INSERT INTO CLOTHES (PRODUCT_ID, CTYPE, CSIZE, MATERIAL, DESCRIPTION) VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query2, (product_id, clothes.type, clothes.size, clothes.material, clothes.description))
            connection.commit()
"""
    def delete_clothe(conf, key):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM PRODUCTS WHERE (PRODUCT_ID = %s)"
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

"""
