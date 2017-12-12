import psycopg2 as dbapi2
from products import *
from flask import Flask

app = Flask(__name__)

class ProductStore:
    def add_product(conf, products):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO PRODUCTS (PNAME, PKIND, PRICE, USER_ID) VALUES (%s, %s, %f, %d)"""
            cursor.execute(query, (Product.name, Product.kind, Product.price, Product.seller))

            connection.commit()

    def delete_product(conf, id, kind):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM PRODUCTS WHERE (PRODUCT_ID = %d)"
            cursor.execute(query, (id,))

            connection.commit()

    #How additional attributes can be added???
    def update_product(conf, key, name, kind, price, seller):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "UPDATE PRODUCTS SET PNAME = %s, PKIND = %s, PRICE = %f, USER_ID = %d WHERE (PRODUCT_ID = %d)"
            cursor.execute(query, (name, kind, price, seller, key))

            connection.commit()

    def get_product(conf, id):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "SELECT PNAME, PKIND, USER_ID FROM PRODUCTS WHERE PRODUCT_ID = %d"
            cursor.execute(query, (id,))
            name, kind, price, seller = cursor.fetchone()

            if kind == "Homemade Food":
                query = "SELECT QUANTITY, FOOD_KIND, DESCRIPTION FROM HOMEMADE_FOOD WHERE PRODUCT_ID = %d"
                cursor.execute(query, (id,))
                quantity, food_kind, description = cursor.fetchone()
                return HomemadeFood(name, kind, price, seller, quantity, food_kind, description)
            elif kind == "Wooden Craft":
                query = "SELECT CSIZE, COLOUR, CRAFT_KIND, DESCRIPTION FROM WOODEN_CRAFT WHERE PRODUCT_ID = %d"
                cursor.execute(query, (id,))
                size, colour, craft_kind, description = cursor.fetchone()
                return WoodenCraft(name, kind, price, seller, size, colour, craft_kind, description)
            # elif kind == "Knitting Work":

    # Same problem with update
    def get_products(conf, seller_id):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "SELECT PRODUCT_ID, PNAME FROM PRODUCTS WHERE USER_ID = %s ORDER BY PRODUCT_ID"
            cursor.execute(query, (seller_id,))
            products = cursor.fetchall()
        return products

    def get_product(conf, product_id):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "SELECT PNAME, PKIND, NICKNAME FROM PRODUCTS INNER JOIN USERS ON PRODUCTS.USER_ID = USERS.USER_ID WHERE PRODUCT_ID = %s"
            cursor.execute(query, (product_id,))
            (pname, pkind, seller) = cursor.fetchone()
            product = Product(pname, pkind, seller)
        return product

    def delete_product(conf, key):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM PRODUCTS WHERE (PRODUCT_ID = %s)"
            cursor.execute(query, (key,))
            connection.commit()

    def update_name(conf, product_id, new_name):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "UPDATE PRODUCTS SET PNAME = %s WHERE (PRODUCT_ID = %s)"
            cursor.execute(query, (new_name, product_id))
            connection.commit()

