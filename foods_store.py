import psycopg2 as dbapi2
from products import  *
from flask import Flask

app = Flask(__name__)

class FoodStore:
    def add_food(conf, product, foods):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO PRODUCTS (PNAME, PKIND, USER_ID) VALUES (%s, %s, %s)"""
            cursor.execute(query, (product.name, product.kind, product.seller))

            query2 = """SELECT PRODUCT_ID FROM PRODUCTS WHERE PNAME = %s AND PKIND = %s AND USER_ID = %s"""
            cursor.execute(query2, (product.name, product.kind, product.seller))

            for row in cursor:
                product_id = row

            query2 = """INSERT INTO HOMEMADE_FOOD (PRODUCT_ID, PIC, QUANTITY, FOOD_KIND, PRICE, DESCRIPTION) VALUES (%s, %s, %f, %s, %s, %s)"""
            cursor.execute(query2, (product_id, foods.pic_link, foods.quantity, foods.food_kind, foods.price, foods.description))
            connection.commit()

    def delete_food(conf, product_id):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM PRODUCTS WHERE (PRODUCT_ID = %d)"
            cursor.execute(query, (id,))
        connection.commit()

    def update_product(conf, key, name, kind, price, seller):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "UPDATE PRODUCTS SET PNAME = %s, PKIND = %s, PRICE = %f, USER_ID = %d WHERE (PRODUCT_ID = %d)"
            cursor.execute(query, (name, kind, price, seller, key))
            connection.commit()

    def get_food(conf, product_id):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "SELECT PIC, QUANTITY, FOOD_KIND, PRICE, DESCRIPTION FROM HOMEMADE_FOOD WHERE PRODUCT_ID = %s"
            cursor.execute(query, (product_id,))
            (pic_link, quantity, food_kind, price, description) = cursor.fetchone()
            food = HomemadeFood(pic_link, quantity, food_kind, price, description)
            return food

    def get_foods(conf):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = """SELECT PRODUCTS.PRODUCT_ID, PNAME, PIC, NICKNAME, PRICE FROM PRODUCTS INNER JOIN HOMEMADE_FOOD ON PRODUCTS.PRODUCT_ID = HOMEMADE_FOOD.PRODUCT_ID
                                INNER JOIN USERS ON PRODUCTS.USER_ID = USERS.USER_ID"""
            cursor.execute(query,)
            foods = cursor.fetchall()
        return foods

