class Product:
    def __init__(self, name, kind, seller):
        self.name = name
        self.kind = kind
        self.seller = seller

class HomemadeFood():
    def __init__(self, pic, quantity, food_kind, price, description):
        self.pic = pic
        self.quantity = quantity
        self.food_kind = food_kind
        self.price = price
        self.description = description

class WoodenCraft():
    def __init__(self, pic, size, colour, craft_kind, price, description):
        self.pic = pic
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

class Accessory():
    def __init__(self, pic, colour, kind, price, description):
        self.pic = pic
        self.colour = colour
        self.kind = kind
        self.price = price
        self.description = description