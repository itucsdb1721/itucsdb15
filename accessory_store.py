import psycopg2 as dbapi2
from products import  *
from flask import Flask

app = Flask(__name__)

class AccessoryStore:
    def add_accessory(conf, product, accessories):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO PRODUCTS (PNAME, PKIND, USER_ID) VALUES (%s, %s, %s)"""
            cursor.execute(query, (product.name, product.kind, product.seller))

            query2 = """SELECT PRODUCT_ID FROM PRODUCTS WHERE PNAME = %s AND PKIND = %s AND USER_ID = %s"""
            cursor.execute(query2, (product.name, product.kind, product.seller))

            for row in cursor:
                product_id = row

            query2 = """INSERT INTO ACCESSORY (PRODUCT_ID, PIC, COLOUR, KIND, PRICE, DESCRIPTION) VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(query2, (product_id, accessories.pic, accessories.colour, accessories.kind, accessories.price, accessories.description))
            connection.commit()

    def delete_accessory(conf, product_id):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM ACCESSORY WHERE (PRODUCT_ID = %s)"
            cursor.execute(query, (product_id,))
            connection.commit()

    def update_accessory(conf, product_id, new_accessory):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "UPDATE ACCESSORY SET PIC = %s, COLOUR = %s, KIND = %s, PRICE = %s, DESCRIPTION = %s WHERE (PRODUCT_ID = %s)"
            cursor.execute(query, (new_accessory.pic, new_accessory.colour, new_accessory.kind, new_accessory.price, new_accessory.description, product_id))
            connection.commit()

    def get_accessory(conf, product_id):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "SELECT PIC, COLOUR, KIND, PRICE, DESCRIPTION FROM ACCESSORY WHERE PRODUCT_ID = %s"
            cursor.execute(query, (product_id,))
            (pic, colour, kind, price, description) = cursor.fetchone()
            accessory = Accessory(pic, colour, kind, price, description)
            return accessory

    def get_accessories(conf):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = """SELECT PRODUCTS.PRODUCT_ID, PNAME, PIC, NICKNAME, PRICE FROM PRODUCTS INNER JOIN ACCESSORY ON PRODUCTS.PRODUCT_ID = ACCESSORY.PRODUCT_ID
                                INNER JOIN USERS ON PRODUCTS.USER_ID = USERS.USER_ID"""
            cursor.execute(query,)
            accesories = cursor.fetchall()
        return accesories

