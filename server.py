import datetime
import json
import os
import psycopg2 as dbapi2
import re

from flask import Flask, Blueprint, flash
from flask import redirect, request, session
from flask import render_template
from flask.helpers import url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from passlib.apps import custom_app_context as pwd_context
from users import User, hashing
from store import Store
from products import *
from clothes_store import ClotheStore
from products_store import ProductStore
from comment_store import CommentStore, Comment
from foods_store import FoodStore

app = Flask(__name__)
app.secret_key = 'helloworld'

def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn

lm = LoginManager()

@lm.user_loader
def load_user(user_id):
    return Store.get_user(app.config['dsn'],user_id)

@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/initdb')
def initialize_database():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS USERS, PRODUCTS, COMMENTS, HOMEMADE_FOOD, CLOTHES, WOODEN_CRAFT CASCADE"""
        cursor.execute(query)

        query = """CREATE TABLE USERS (
                                 USER_ID SERIAL PRIMARY KEY,
                                 NM VARCHAR(80) NOT NULL,
                                 SURNAME VARCHAR(80) NOT NULL,
                                 NICKNAME VARCHAR(80) NOT NULL,
                                 EMAIL VARCHAR(80) NOT NULL,
                                 PASSWORD VARCHAR(200) NOT NULL
                                 )"""
        cursor.execute(query)

        query = """CREATE TABLE PRODUCTS (
                                         PRODUCT_ID SERIAL PRIMARY KEY,
                                         PNAME CHARACTER(40),
                                         PKIND VARCHAR(100) NOT NULL,
                                         USER_ID INTEGER NOT NULL REFERENCES USERS(USER_ID) ON DELETE CASCADE
                                         )"""
        cursor.execute(query)

        query = """CREATE TABLE COMMENTS (
                                          COMMENT_ID SERIAL PRIMARY KEY,
                                          USER_ID SERIAL REFERENCES USERS(USER_ID) ON DELETE CASCADE,
                                          PRODUCT_ID SERIAL REFERENCES PRODUCTS(PRODUCT_ID) ON DELETE CASCADE,
                                          COMMENT VARCHAR(200) NOT NULL
                                          )"""
        cursor.execute(query)

        query = """CREATE TABLE HOMEMADE_FOOD (
                                 PRODUCT_ID SERIAL PRIMARY KEY REFERENCES PRODUCTS(PRODUCT_ID) ON DELETE CASCADE,
                                 PIC TEXT,
                                 QUANTITY REAL,
                                 FOOD_KIND VARCHAR(100) NOT NULL,
                                 PRICE VARCHAR(10),
                                 DESCRIPTION TEXT
                                 )"""
        cursor.execute(query)

        query = """CREATE TABLE CLOTHES (
                                         PRODUCT_ID SERIAL PRIMARY KEY REFERENCES PRODUCTS(PRODUCT_ID) ON DELETE CASCADE,
                                         PIC TEXT,
                                         CTYPE VARCHAR(50) NOT NULL,
                                         CSIZE VARCHAR(20) NOT NULL,
                                         MATERIAL VARCHAR(20) NOT NULL,
                                         PRICE VARCHAR(10),
                                         DESCRIPTION TEXT
                                         )"""
        cursor.execute(query)

        query = """CREATE TABLE WOODEN_CRAFT (
                                 PRODUCT_ID SERIAL PRIMARY KEY REFERENCES PRODUCTS(PRODUCT_ID) ON DELETE CASCADE,
                                 PIC TEXT,
                                 CSIZE INTEGER,
                                 COLOUR CHARACTER(40),
                                 CRAFT_KIND VARCHAR(100) NOT NULL,
                                 PRICE VARCHAR(10),
                                 DESCRIPTION TEXT
                                 )"""
        cursor.execute(query)

        connection.commit()

    return redirect(url_for('home_page'))


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

    else:
        return render_template('list_users_product.html')

@app.route('/delete_comment=<int:comment_id>=<int:product_id>')
def delete_comment(comment_id, product_id):
    CommentStore.delete_comment(app.config['dsn'], comment_id)
    return redirect(url_for('product_page', product_id = product_id))

@app.route('/update_comment=<int:comment_id>=<int:product_id>=<string:old_comment>', methods = ['GET', 'POST'])
def update_comment(comment_id, old_comment, product_id):
    if request.method == 'GET':
        return render_template('update_comment.html', old_comment = old_comment)
    new_comment = request.form['user_comment']
    CommentStore.update_comment(app.config['dsn'], comment_id, new_comment)
    return redirect(url_for('product_page', product_id=product_id))

@app.route('/delete_product=<int:product_id>')
def delete_product(product_id):
    ProductStore.delete_product(app.config['dsn'], product_id)
    return render_template('list_users_product.html')

@app.route('/add_homemade_foods', methods=['GET', 'POST'])
@login_required
def add_homemade_foods():
    if request.method == 'GET':
        return render_template('homemade_food_edit.html')

    seller_id = Store.get_userid(app.config['dsn'], current_user.nickname)

    product = Product(request.form['name'], "homemade_food", seller_id)
    homemade_food = HomemadeFood(request.form['pic'], request.form['quantity'], request.form['food_kind'], request.form['price'], request.form['description'])
    FoodStore.add_food(app.config['dsn'], product, homemade_food)

    return redirect(url_for('home_page'))

if __name__ == '__main__':
    lm.init_app(app)
    lm.login_view = 'login'
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='postgres' password='vagrant'
                                        host='localhost' port=5432 dbname='database'"""

    app.run(host='localhost', port=port, debug=debug)

