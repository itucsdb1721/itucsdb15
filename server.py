import datetime
import json
import os
import psycopg2 as dbapi2
import re

from flask import Flask, Blueprint, flash
from flask import redirect, request, session
from flask import render_template
from flask.helpers import url_for
from flask_login import LoginManager, login_user, logout_user, current_user
from passlib.apps import custom_app_context as pwd_context
from users import User, hashing
from store import Store

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
    if Store.get_user(app.config['dsn'],user_id):
        return Store.get_user(app.config['dsn'],user_id)
    else:
        return redirect(url_for('home_page'))

@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/initdb')
def initialize_database():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS USERS CASCADE"""
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
                                         PRICE REAL,
                                         USER_ID INTEGER NOT NULL REFERENCES USERS(USER_ID) ON DELETE CASCADE
                                         )"""
        cursor.execute(query)

        query = """CREATE TABLE COMMENTS (
                                          COMMENT_ID SERIAL PRIMARY KEY,
                                          USER_ID SERIAL REFERENCES USERS(USER_ID) ON DELETE CASCADE,
                                          PRODUCT_ID SERIAL REFERENCES PRODUCTS(PRODUCT_ID) ON DELETE CASCADE,
                                          WRITE_DATE DATE NOT NULL,
                                          COMMENT VARCHAR(200) NOT NULL
                                          )"""
        cursor.execute(query)

        query = """CREATE TABLE HOMEMADE_FOOD (
                                 PRODUCT_ID SERIAL PRIMARY KEY REFERENCES PRODUCTS(PRODUCT_ID) ON DELETE CASCADE,
                                 QUANTITY REAL,
                                 FOOD_KIND VARCHAR(100) NOT NULL,
                                 DESCRIPTION TEXT
                                 )"""
        cursor.execute(query)

        query = """CREATE TABLE CLOTHES (
                                         PRODUCT_ID SERIAL PRIMARY KEY REFERENCES PRODUCTS(PRODUCT_ID) ON DELETE CASCADE,
                                         CLOTHE_TYPE VARCHAR(50) NOT NULL,
                                         SIZE VARCHAR(20) NOT NULL,
                                         MATERIAL VARCHAR(20) NOT NULL,
                                         DESCRIPTION TEXT
                                         )"""
        cursor.execute(query)

        query = """CREATE TABLE WOODEN_CRAFT (
                                 PRODUCT_ID SERIAL PRIMARY KEY REFERENCES PRODUCTS(PRODUCT_ID) ON DELETE CASCADE,
                                 CSIZE INTEGER,
                                 COLOUR CHARACTER(40),
                                 CRAFT_KIND VARCHAR(100) NOT NULL,
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

@app.route('/homemade_foods')
def homemade_foods_page():
    #products = current_app.store.get_products()
    return render_template('homemade_foods.html')#,products = sorted(products.items()))

if __name__ == '__main__':
    lm.init_app(app)
    lm.login_view = 'app.login'
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant'
                                        host='localhost' port=54321 dbname='itucsdb'"""

    app.run(host='0.0.0.0', port=port, debug=debug)

