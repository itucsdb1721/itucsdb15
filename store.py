import psycopg2 as dbapi2
from products import Product


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