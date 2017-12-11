import psycopg2 as dbapi2
from products import Product

class ProductStore:

    def get_products(conf, user_id):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "SELECT PRODUCT_ID, PNAME, PKIND FROM PRODUCTS WHERE USER_ID = %s ORDER BY PRODUCT_ID"
            cursor.execute(query, (user_id),)
            products = cursor.fetchall()
        return products
