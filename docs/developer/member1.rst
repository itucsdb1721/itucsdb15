Parts Implemented by Gamze Akyol
================================

**************
Homemade Foods
**************

Table
-----

Homemade Food table exists in the server.py file.

.. code-block:: sql

       CREATE TABLE HOMEMADE_FOOD (
                    PRODUCT_ID SERIAL PRIMARY KEY REFERENCES PRODUCTS(PRODUCT_ID) ON DELETE CASCADE,
                    PIC TEXT,
                    QUANTITY TEXT,
                    FOOD_KIND VARCHAR(100) NOT NULL,
                    PRICE VARCHAR(10),
                    DESCRIPTION TEXT
       )

PRODUCT_ID attribute references Products table's PRODUCT_ID attribute.

Class
-----

.. code-block:: python

        class HomemadeFood():
              def __init__(self, pic, quantity, food_kind, price, description):
                  self.pic = pic
                  self.quantity = quantity
                  self.food_kind = food_kind
                  self.price = price
                  self.description = description
Class Operations
----------------
Homemade Food's class operations exists in foods_store.py.


- The following database operations are implemented for Homemade Food:

    -Add Operation

.. code-block:: python

       def add_food(conf, product, foods):
              with dbapi2.connect(conf) as connection:
                    cursor = connection.cursor()
                    query = """INSERT INTO PRODUCTS (PNAME, PKIND, USER_ID) VALUES (%s, %s, %s)"""
                    cursor.execute(query, (product.name, product.kind, product.seller))

                   query2 = """SELECT PRODUCT_ID FROM PRODUCTS WHERE PNAME = %s AND PKIND = %s AND USER_ID = %s"""
                   cursor.execute(query2, (product.name, product.kind, product.seller))

                   for row in cursor:
                       product_id = row

                   query2 = """INSERT INTO HOMEMADE_FOOD (PRODUCT_ID, PIC, QUANTITY, FOOD_KIND, PRICE, DESCRIPTION) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
                   cursor.execute(query2, (product_id, foods.pic, foods.quantity, foods.food_kind, foods.price, foods.description))
                   connection.commit()
 
 
Adds Homemade Food to both Products and Homemade Food table.

     -Delete Operation

.. code-block:: python

        def delete_food(conf, product_id):
              with dbapi2.connect(conf) as connection:
                   cursor = connection.cursor()
                   query = "DELETE FROM HOMEMADE_FOOD WHERE (PRODUCT_ID = %s)"
                   cursor.execute(query, (product_id,))
                   connection.commit()

Deletes the Homemade Food that has the given product_id as parameter.

    
      -Update Operations

.. code-block:: python

        def update_food(conf, product_id, new_food):
              with dbapi2.connect(conf) as connection:
                   cursor = connection.cursor()
                   query = "UPDATE HOMEMADE_FOOD SET PIC = %s, QUANTITY = %s, FOOD_KIND = %s, PRICE = %s, DESCRIPTION = %s 
                   WHERE (PRODUCT_ID = %s)"
                   cursor.execute(query, (new_food.pic, new_food.quantity, new_food.food_kind, new_food.price, new_food.description,                        product_id))
                   connection.commit()

Update an attribute of a homemade food.

      -Select Operations

.. code-block:: python

        def get_food(conf, product_id):
              with dbapi2.connect(conf) as connection:
                   cursor = connection.cursor()
                   query = "SELECT PIC, QUANTITY, FOOD_KIND, PRICE, DESCRIPTION FROM HOMEMADE_FOOD WHERE PRODUCT_ID = %s"
                   cursor.execute(query, (product_id,))
                   (pic, quantity, food_kind, price, description) = cursor.fetchone()
                   food = HomemadeFood(pic, quantity, food_kind, price, description)
                   return food

Selects Homemade Food by product_id.

.. code-block:: python

    def get_foods(conf):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = """SELECT PRODUCTS.PRODUCT_ID, PNAME, PIC, NICKNAME, PRICE FROM PRODUCTS INNER JOIN HOMEMADE_FOOD ON                             PRODUCTS.PRODUCT_ID = HOMEMADE_FOOD.PRODUCT_ID
            INNER JOIN USERS ON PRODUCTS.USER_ID = USERS.USER_ID"""
            cursor.execute(query,)
            foods = cursor.fetchall()
            return foods
            
Selects all the Homemade Foods.

Templates
---------
**homemade_food_edit.html**, **homemade_foods.html** and **list_foods.html** **update_foods.html** are the related templates to Homemade Food.

GET/POST Operations
-------------------
server.py

.. code-block:: python

       @app.route('/add_homemade_foods', methods=['GET', 'POST'])
       @login_required
       def add_homemade_foods():
              if request.method == 'GET':
                     return render_template('homemade_food_edit.html')

              seller_id = Store.get_userid(app.config['dsn'], current_user.nickname)

              product = Product(request.form['name'], "homemade_food", seller_id)
              homemade_food = HomemadeFood(request.form['pic'], request.form['quantity'], request.form['food_kind'],                                   request.form['price'], request.form['description'])
              FoodStore.add_food(app.config['dsn'], product, homemade_food)

              return redirect(url_for('home_page'))

       @app.route('/list_foods', methods=['GET', 'POST'])
       def list_foods():
              if request.method == 'GET':
                     homemade_food = FoodStore.get_foods(app.config['dsn'])
                     return render_template('list_foods.html', homemade_food = homemade_food)

Homemade food specific functions are given above with GET/POST operations.

*************
Wooden Crafts
*************

***********
Accessories
***********
