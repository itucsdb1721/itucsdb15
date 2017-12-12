import psycopg2 as dbapi2
from products import *
from flask import Flask

app = Flask(__name__)


class WoodStore:
    def add_woodencraft(conf, product, wooden_craft):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO PRODUCTS (PNAME, PKIND, USER_ID) VALUES (%s, %s, %s)"""
            cursor.execute(query, (product.name, product.kind, product.seller))

            query2 = """SELECT PRODUCT_ID FROM PRODUCTS WHERE PNAME = %s AND PKIND = %s AND USER_ID = %s"""
            cursor.execute(query2, (product.name, product.kind, product.seller))

            for row in cursor:
                product_id = row

            query2 = """INSERT INTO WOODEN_CRAFT (PRODUCT_ID, PIC, CSIZE, COLOUR, CRAFT_KIND, PRICE, DESCRIPTION) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query2, (product_id, wooden_craft.pic, wooden_craft.size, wooden_craft.colour, wooden_craft.craft_kind, wooden_craft.price, wooden_craft.description))
            connection.commit()

    def delete_woodencraft(conf, product_id):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM WOODEN_CRAFT WHERE (PRODUCT_ID = %s)"
            cursor.execute(query, (product_id,))
            connection.commit()

    def update_woodencraft(conf, product_id, new_craft):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "UPDATE WOODEN_CRAFT SET PIC = %s, CSIZE = %s, COLOUR = %s, CRAFT_KIND = %s, PRICE = %s, DESCRIPTION = %s WHERE (PRODUCT_ID = %s)"
            cursor.execute(query, (new_craft.pic, new_craft.size, new_craft.colour, new_craft.craft_kind, new_craft.price, new_craft.description, product_id))
            connection.commit()

    def get_woodencraft(conf, product_id):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "SELECT PIC, CSIZE, COLOUR, CRAFT_KIND, PRICE, DESCRIPTION FROM WOODEN_CRAFT WHERE PRODUCT_ID = %s"
            cursor.execute(query, (product_id,))
            (pic, size, colour, craft_kind, price, description) = cursor.fetchone()
            craft = WoodenCraft(pic, size, colour, craft_kind, price, description)
            return craft

    def get_woodencrafts(conf):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = """SELECT PRODUCTS.PRODUCT_ID, PNAME, PIC, NICKNAME, PRICE FROM PRODUCTS INNER JOIN WOODEN_CRAFT ON PRODUCTS.PRODUCT_ID = WOODEN_CRAFT.PRODUCT_ID
                                INNER JOIN USERS ON PRODUCTS.USER_ID = USERS.USER_ID"""
            cursor.execute(query, )
            crafts = cursor.fetchall()
        return crafts

