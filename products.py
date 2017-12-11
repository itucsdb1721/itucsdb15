class Product:
    def __init__(self, name, kind, seller):
        self.name = name
        self.kind = kind
        self.seller = seller

class HomemadeFood():
    def __init__(self, pic_link, quantity, food_kind, price, description):
        self.pic_link = pic_link
        self.quantity = quantity
        self.food_kind = food_kind
        self.price = price
        self.description = description

class WoodenCraft():
    def __init__(self, pic_link, size, colour, craft_kind, price, description):
        self.pic_link = pic_link
        self.size = size
        self.colour = colour
        self.craft_kind = craft_kind
        self.price = price
        self.description = description

class Clothes():
    def __init__(self, pic_link, type, size, material, price, description):
        self.pic_link = pic_link
        self.type = type
        self.size = size
        self.material = material
        self.price = price
        self.description = description