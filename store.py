import psycopg2 as dbapi2
from products import Product
from users import User


class Store:
    def __init__(self, dbfile):
        self.dbfile = dbfile
        self.last_key = None

    def add_product(self, product):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO product (ID, PNAME, QUANTITY, KIND, ALLERGENS, SELLER) VALUES (?, ?, ?, ?, ?, ?)"
            cursor.execute(query, (product.name, product.quantity, product.kind, product.allergens, product.seller))
            connection.commit()
            self.last_key = cursor.lastrowid

    def delete_product(self, key):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM product WHERE (ID = ?)"
            cursor.execute(query, (key,))
            connection.commit()

    def update_product(self, key, name, quantity, kind, allergens, seller):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "UPDATE product SET PNAME = ?, QUANTITY = ?, KIND = ?, ALLERGENS = ?, SELLER = ?, WHERE (ID = ?)"
            cursor.execute(query, (name, quantity, kind, allergens, seller, key))
            connection.commit()

    def get_product(self, key):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT PNAME, QUANTITY, KIND, ALLERGENS, SELLER FROM product WHERE (ID = ?)"
            cursor.execute(query, (key,))
            name, quantity, kind, allergens, seller = cursor.fetchone()
        return Product(name, quantity, kind, allergens, seller)

    def get_products(self):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT ID, PNAME, QUANTITY, KIND, ALLERGENS, SELLER FROM product ORDER BY ID"
            cursor.execute(query)
            products = [(key, Product(name, quantity, kind, allergens, seller))
                        for key, name, quantity, kind, allergens, seller in cursor]
        return products
    
    def add_user(self, users):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO USERS (NAME, SURNAME, NICKNAME, EMAIL, PASSWORD ) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(query, (users.name, users.surname, users.nickname, users.email, users.password))
            connection.commit()
            self.last_key = cursor.lastrowid

    def delete_user(self, key):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM USERS WHERE (ID = ?)"
            cursor.execute(query, (key,))
            connection.commit()

    def update_user(self, key, name, surname, nickname, email, password):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "UPDATE USERS SET NAME = ?,SURNAME = ?, NICKNAME = ?, EMAIL = ?, PASSWORD = ? WHERE (ID = ?)"
            cursor.execute(query, (name, surname, nickname, email, password, key))
            connection.commit()

    def get_user(self, key):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT NAME, SURNAME, NICKNAME, EMAIL, PASSWORD FROM USERS WHERE (ID = ?)"
            cursor.execute(query, (key,))
            name, surname, nickname, email, password = cursor.fetchone()
        return User(name, surname, nickname, email, password)

    def get_users(self):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT ID, NAME, SURNAME, NICKNAME, EMAIL, PASSWORD FROM USERS ORDER BY ID"
            cursor.execute(query)
            users = [(key, User(name, surname, nickname, email, password))
                      for key, name, surname, nickname, email, password in cursor]
        return users
