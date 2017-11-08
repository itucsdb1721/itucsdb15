from flask import Flask

from handlers import site
from products import Product
from store import Store

import os

def create_app():
    app = Flask(__name__)
    app.config.from_object('settings')
    app.register_blueprint(site)

    return app

def main():
    app = create_app()
    #debug = app.config['DEBUG']
    #app.store = Store(os.path.join("\\", "products.sql"))
    port = app.config.get('PORT', 8080)
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
