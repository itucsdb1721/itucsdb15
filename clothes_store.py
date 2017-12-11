import psycopg2 as dbapi2
from products import Product, Clothes

class ClotheStore:
    def add_clothe(conf, product, clothes):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query2 = """INSERT INTO PRODUCTS (PNAME, PKIND, USER_ID) VALUES (%s, %s, %s)"""
            cursor.execute(query2, (product.name, product.kind, product.seller))

            query2 = """SELECT PRODUCT_ID FROM PRODUCTS WHERE PNAME = %s AND PKIND = %s AND USER_ID = %s"""
            cursor.execute(query2, (product.name, product.kind, product.seller))

            for row in cursor:
                product_id = row

            query2 = """INSERT INTO CLOTHES (PRODUCT_ID, PIC, CTYPE, CSIZE, MATERIAL, PRICE, DESCRIPTION) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query2, (product_id, clothes.pic_link, clothes.type, clothes.size, clothes.material, clothes.price, clothes.description))
            connection.commit()

    def get_clothe(conf, product_id):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "SELECT PIC, CTYPE, CSIZE, MATERIAL, PRICE, DESCRIPTION FROM CLOTHES WHERE PRODUCT_ID = %s"
            cursor.execute(query, (product_id,))
            (pic, ctype, csize, material, price, description) = cursor.fetchone()
            clothe = Clothes(pic, ctype, csize, material, price, description)
            return clothe

    def get_clothes(conf):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = """SELECT PRODUCTS.PRODUCT_ID, PNAME, PIC, NICKNAME, PRICE FROM PRODUCTS INNER JOIN CLOTHES ON PRODUCTS.PRODUCT_ID = CLOTHES.PRODUCT_ID
                    INNER JOIN USERS ON PRODUCTS.USER_ID = USERS.USER_ID"""
            cursor.execute(query,)
            clothes = cursor.fetchall()
        return clothes

    def update_clothe(conf, product_id, new_clothe):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "UPDATE CLOTHES SET PIC = %s, CTYPE = %s, CSIZE = %s, MATERIAL = %s, PRICE = %s, DESCRIPTION = %s WHERE (PRODUCT_ID = %s)"
            cursor.execute(query, (new_clothe.pic_link, new_clothe.type, new_clothe.size, new_clothe.material, new_clothe.price, new_clothe.description, product_id))
            connection.commit()



