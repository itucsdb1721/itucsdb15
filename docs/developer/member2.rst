Parts Implemented by Şeymanur Aktı
================================

**************
Clothes
**************

Table
-----

Clothes table exists in the server.py file.

.. code-block:: sql

       CREATE TABLE CLOTHES (
                                         PRODUCT_ID SERIAL PRIMARY KEY REFERENCES PRODUCTS(PRODUCT_ID) ON DELETE CASCADE,
                                         PIC TEXT,
                                         CTYPE VARCHAR(50) NOT NULL,
                                         CSIZE VARCHAR(20) NOT NULL,
                                         MATERIAL VARCHAR(20) NOT NULL,
                                         PRICE VARCHAR(10),
                                         DESCRIPTION TEXT
                                         )

PRODUCT_ID attribute references Products table's PRODUCT_ID attribute. When a clothe is deleted, it is deleted from Products table by using its ID, thus it is deleted from CLOTHES table because of ON DELETE CASCADE property.

Class
-----

.. code-block:: python

        class Clothes():
            def __init__(self, pic_link, type, size, material, price, description):
                self.pic_link = pic_link
                self.type = type
                self.size = size
                self.material = material
                self.price = price
                self.description = description

Class Operations
----------------
Clothe's class operations exists in clothes_store.py.


- The following database operations are implemented for Clothes:

    -Add Operation

.. code-block:: python

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
 
 
Adds Clothe to both Products and Clothe table.

     -Delete Operation

.. code-block:: python

        def delete_product(conf, key):
            with dbapi2.connect(conf) as connection:
                cursor = connection.cursor()
                query = "DELETE FROM PRODUCTS WHERE (PRODUCT_ID = %s)"
                cursor.execute(query, (key,))
                connection.commit()

Delete operation is done by using PRODUCTS table which keeps all of the products' id's.

    
      -Update Operations

.. code-block:: python

    def update_clothe(conf, product_id, new_clothe):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "UPDATE CLOTHES SET PIC = %s, CTYPE = %s, CSIZE = %s, MATERIAL = %s, PRICE = %s, DESCRIPTION = %s WHERE (PRODUCT_ID = %s)"
            cursor.execute(query, (new_clothe.pic_link, new_clothe.type, new_clothe.size, new_clothe.material, new_clothe.price, new_clothe.description, product_id))
            connection.commit()

Update any attribute of a clothe.

      -Select Operations

.. code-block:: python

    def get_clothe(conf, product_id):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "SELECT PIC, CTYPE, CSIZE, MATERIAL, PRICE, DESCRIPTION FROM CLOTHES WHERE PRODUCT_ID = %s"
            cursor.execute(query, (product_id,))
            (pic, ctype, csize, material, price, description) = cursor.fetchone()
            clothe = Clothes(pic, ctype, csize, material, price, description)
            return clothe

Selects a clothe by its product_id.

.. code-block:: python

    def get_clothes(conf):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = """SELECT PRODUCTS.PRODUCT_ID, PNAME, PIC, NICKNAME, PRICE FROM PRODUCTS INNER JOIN CLOTHES ON PRODUCTS.PRODUCT_ID = CLOTHES.PRODUCT_ID
                    INNER JOIN USERS ON PRODUCTS.USER_ID = USERS.USER_ID"""
            cursor.execute(query,)
            clothes = cursor.fetchall()
        return clothes
            
Selects all clothes, used for listing clothes page.

Templates
---------
**add_clothes.html**, **clothe_page.html** and **list_clothes.html** **update_clothe.html** are the related templates to Clothes.

GET/POST Operations
-------------------
server.py

.. code-block:: python

    @app.route('/add_clothes', methods=['GET', 'POST'])
    @login_required
    def add_clothes():
        if request.method == 'GET':
            return render_template('add_clothes.html')
            seller_id = Store.get_userid(app.config['dsn'], current_user.nickname)
            product = Product(request.form['name'], "clothe", seller_id)
            clothe = Clothes(request.form['pic'], request.form['type'], request.form['size'], request.form['material'], request.form['price'], request.form['description'])
            ClotheStore.add_clothe(app.config['dsn'], product, clothe)
            return redirect(url_for('home_page'))

      @app.route('/list_clothes', methods=['GET', 'POST'])
       def list_clothes():
            if request.method == 'GET':
            clothes = ClotheStore.get_clothes(app.config['dsn'])
            return render_template('list_clothes.html', clothes = clothes)
            
            
       @app.route('/update_product=<int:product_id>', methods=['GET', 'POST'])
       def update_product(product_id):
          product = ProductStore.get_product(app.config['dsn'], product_id)
          if product.kind == 'clothe':
              clothe = ClotheStore.get_clothe(app.config['dsn'], product_id)
              if request.method == 'GET':
                  return render_template('update_clothe.html', productname=product.name, clothe = clothe)
              new_clothe = Clothes(request.form['pic'], request.form['type'], request.form['size'], request.form['material'], request.form['price'], request.form['description'])
              new_name = request.form['name']
              ClotheStore.update_clothe(app.config['dsn'], product_id, new_clothe)
              ProductStore.update_name(app.config['dsn'], product_id, new_name)
              return redirect(url_for('list_products'))
           
           
        @app.route('/product_page=<int:product_id>', methods = ['GET', 'POST'])
        def product_page(product_id):
            product = ProductStore.get_product(app.config['dsn'], product_id)
            if (product.kind == "clothe"):
             clothe = ClotheStore.get_clothe(app.config['dsn'], product_id)
             comments = CommentStore.get_comment_for_product(app.config['dsn'], product_id)
             if request.method == 'GET':
                  return render_template('clothe_page.html', product = product, clothe = clothe, comments = comments, product_id = product_id)
             get_comment = request.form['user_comment']
             if get_comment:
                user_id = Store.get_userid(app.config['dsn'], current_user.nickname)
                comment = Comment(user_id, product_id, get_comment)
                CommentStore.add_comment(app.config['dsn'], comment)
                return redirect(url_for('product_page', product_id = product_id))
           
Clothe related functions are given above with GET/POST operations.

*************
Users
*************
Table
-----

Users table exists in the server.py file.

.. code-block:: sql

       CREATE TABLE USERS (
                                 USER_ID SERIAL PRIMARY KEY,
                                 NM VARCHAR(80) NOT NULL,
                                 SURNAME VARCHAR(80) NOT NULL,
                                 NICKNAME VARCHAR(80) NOT NULL,
                                 EMAIL VARCHAR(80) NOT NULL,
                                 PASSWORD VARCHAR(200) NOT NULL
                                 )

Class
-----

.. code-block:: python

    class User():
        def __init__(self, name, surname, nickname, email, password):
            self.nickname = nickname
            self.password = hashing(password)
            self.name = name
            self.surname = surname
            self.email = email
            self.authenticated = True

        def get_id(self):
            return self.nickname

        def is_authenticated(self):
            return self.authenticated

        @property
            def is_active(self):
               return True

        def hashing(password):
            secret_key = 'helloworld'
            return pwd_context.encrypt(password)
            
            
Passwords are keeping as hashed.

Class Operations
----------------
User's class operations exists in store.py.


- The following database operations are implemented for Users:

    -Add Operation

.. code-block:: python

    def add_user(conf, users):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query2 = """INSERT INTO USERS (NM, SURNAME, NICKNAME, EMAIL, PASSWORD ) VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query2, (users.name, users.surname, users.nickname, users.email, users.password))
            connection.commit()
 
 
Adds user to User table.

     -Delete Operation

.. code-block:: python

    def delete_user(conf, key):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM USERS WHERE (USER_ID = %s)"
            cursor.execute(query, (key,))
            connection.commit()

Deletes user from USERS table.
    
      -Update Operations

.. code-block:: python

    def update_password(conf, username, new_password):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "UPDATE USERS SET PASSWORD = %s WHERE (NICKNAME = %s)"
            cursor.execute(query, (new_password, username))
            connection.commit()

Update operation is only valid for password.

      -Select Operations

.. code-block:: python

    def get_user(conf, username):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "SELECT NM, SURNAME, NICKNAME, EMAIL, PASSWORD FROM USERS WHERE NICKNAME = %s"
            cursor.execute(query, (username,))
            for row in cursor:
                (name, surname, nickname, email, password) = row
                return User(name, surname, nickname, email, password)

Selects a user by its user_id.

.. code-block:: python

    def get_userid(conf, username):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "SELECT USER_ID FROM USERS WHERE NICKNAME = %s"
            cursor.execute(query, (username,))
            for row in cursor:
                user_id = row
                return user_id
            
Selects user_id by using nickname.

.. code-block:: python

    def get_users(conf):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "SELECT USER_ID, NM, SURNAME, NICKNAME, EMAIL, PASSWORD FROM USERS ORDER BY USER_ID"
            cursor.execute(query)
            users = cursor.fetchall()
            return users

            
Selects all users

.. code-block:: python

    def is_exist(conf, username):
        with dbapi2.connect(conf) as connection:
            cursor = connection.cursor()
            query = "SELECT PASSWORD FROM USERS WHERE NICKNAME = %s"
            cursor.execute(query, (username,))
            for row in cursor:
                (hashed,) = row
                return hashed
           
Controls if user is exist in table and returns its password for login.

Templates
---------
**register.html**, **login.html**, **list_users_product.html**, **change_password.html** and **delete_account.html** are the related templates to Users.

GET/POST Operations
-------------------
server.py

.. code-block:: python

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'GET':
            return render_template('register.html')
            #if (request.form['password'] == request.form['password2']):
            user = User(request.form['name'], request.form['surname'], request.form['nickname'], request.form['email'], request.form['password'])
             #else:
    #    return render_template('register.html', error2="Enter password again.")
            if Store.is_exist(app.config['dsn'], request.form['nickname']):
                return render_template('register.html', error = "This username is already taken.")
                Store.add_user(app.config['dsn'], user)
                return redirect(url_for('login'))

     @app.route('/login', methods=['GET', 'POST'])
     def login():
        if request.method == 'GET':
            return render_template('login.html')
        username = request.form['username']
        password = request.form['password']
        truepassword = Store.is_exist(app.config['dsn'], username)
        if truepassword:
             user = Store.get_user(app.config['dsn'], username)
             if pwd_context.verify(password, truepassword):
                login_user(user)
                return redirect(url_for('home_page'))
             else:
                return redirect(url_for('login'))

        else:
             return redirect(url_for('login'))

       @app.route('/logout')
       def logout_page():
              logout_user()
              flash('You have logged out.')
              return redirect(url_for('home_page'))

       @app.route('/account')
       def account():
              return render_template('account.html')

       @app.route('/list_products')
       def list_products():
              user_id = Store.get_userid(app.config['dsn'], current_user.nickname)
              products = ProductStore.get_products(app.config['dsn'], user_id)
              return render_template('list_users_product.html', products=products)

       @app.route('/change_password', methods=['GET', 'POST'])
       def change_password():
              if request.method == 'GET':
                     return render_template('change_password.html')
              oldpassword = request.form['oldpassword']
              truepassword = Store.is_exist(app.config['dsn'], current_user.nickname)
              if pwd_context.verify(oldpassword, truepassword):
                     if (request.form['newpassword'] == request.form['newpassword2']):
                            Store.update_password(app.config['dsn'], current_user.nickname, hashing(request.form['newpassword']))
                     else:
                            return render_template('change_password.html', error2 = 'Enter the new password again.')
              else:
                     return render_template('change_password.html', error1='Wrong password.')

              return redirect(url_for('account'))

        @app.route('/delete_account', methods=['GET', 'POST'])
        def delete_account():
        if request.method == 'GET':
              return render_template('delete_account.html')
        entered_password = request.form['password']
        truepassword = Store.is_exist(app.config['dsn'], current_user.nickname)
        if pwd_context.verify(entered_password, truepassword):
              user_id = Store.get_userid(app.config['dsn'], current_user.nickname)
              logout_user()
              Store.delete_user(app.config['dsn'], user_id)
              return redirect(url_for('home_page'))
        else:
              return render_template('delete_account.html', error = 'Wrong password.')
           
User related functions are given above with GET/POST operations.


***********
Comments
***********
