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

            if products.kind == "Homemade Food":
                query = """INSERT INTO HOMEMADE_FOOD (QUANTITY, FOOD_KIND, DESCRIPTION) VALUES (%f, %s, %s)"""
                cursor.execute(query, (HomemadeFood.quantity, HomemadeFood.food_kind, HomemadeFood.description))
            elif products.kind == "Wooden Craft":
                query = """INSERT INTO WOODEN_CRAFT (CSIZE, COLOUR, CRAFT_KIND, DESCRIPTION) VALUES (%s, %s, %s, %s)"""
                cursor.execute(query, (WoodenCraft.size, WoodenCraft.colour, WoodenCraft.craft_kind, WoodenCraft.description))
            #elif products.kind == "Knitting Work":

            connection.commit()

    def delete_product(conf, id, kind):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM PRODUCTS WHERE (PRODUCT_ID = %d)"
            cursor.execute(query, (id,))

            if kind == "Homemade Food":
                query = "DELETE FROM HOMEMADE_FOOD WHERE (PRODUCT_ID = %d)"
                cursor.execute(query, (id,))
            elif kind == "Wooden Craft":
                query = "DELETE FROM WOODEN_CRAFT WHERE (PRODUCT_ID = %d)"
                cursor.execute(query, (id,))

        connection.commit()

    #How additional attributes can be added???
    def update_product(conf, key, name, kind, price, seller):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "UPDATE PRODUCTS SET PNAME = %s, PKIND = %s, PRICE = %f, USER_ID = %d WHERE (PRODUCT_ID = %d)"
            cursor.execute(query, (name, kind, price, seller, key))

            if kind == "Homemade Food":
                query = """UPDATE HOMEMADE_FOOD SET QUANTITY = %f, FOOD_KIND = %s, DESCRIPTION = %s WHERE (PRODUCT_ID = %d)"""
                cursor.execute(query, (HomemadeFood.quantity, HomemadeFood.food_kind, HomemadeFood.description))
            elif kind == "Wooden Craft":
                query = """UPDATE WOODEN_CRAFT SET CSIZE = %d, COLOUR = %s, CRAFT_KIND = %s, DESCRIPTION = %s WHERE (PRODUCT_ID = %d)"""
                cursor.execute(query, (WoodenCraft.size, WoodenCraft.colour, WoodenCraft.craft_kind, WoodenCraft.description))
            # elif kind == "Knitting Work":

            connection.commit()

    def get_product(conf, id):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "SELECT PNAME, PKIND, PRICE, USER_ID FROM PRODUCTS WHERE PRODUCT_ID = %d"
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
    def get_products(conf):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "SELECT PRODUCT_ID, PNAME, PKIND, PRICE, USER_ID FROM PRODUCTS ORDER BY PRODUCT_ID"
            cursor.execute(query)
            products = [(id, Product(name, kind, price, seller))
                      for id, name, kind, price, seller in cursor]
        return products



