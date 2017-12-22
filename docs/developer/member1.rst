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
