from flask import Blueprint, render_template
from flask import current_app

from flask import request

from datetime import datetime

from users import User

site = Blueprint('site', __name__)


@site.route('/')
def home_page():
    now = datetime.now()
    day = now.strftime('%A')
    return render_template('index.html', day_name=day)


@site.route('/products')
def products_page():
    products = current_app.store.get_products()
    return render_template('products.html', products = sorted(products.items()))

@site.route('/product/<int:product_id>')
def product_page(product_id):
    product = current_app.store.get_product(product_id)
    return render_template('product.html', product=product)


@site.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = User(request.form['name'] , request.form['surname'], request.form['nickname'], request.form['password'], request.form['email'])
    #db.session.add(user)
    #db.session.commit()
    #^^flash('Registration is successful!!')
    return redirect('home.html')
