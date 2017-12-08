class Product:
    def __init__(self, name, kind, price, seller):
        self.name = name
        self.kind = kind
        self.price = price
        self.seller = seller

class HomemadeFood(Product):
    def __init__(self, quantity, food_kind, description):
        self.quantity = quantity
        self.food_kind = food_kind
        self.description = description

class WoodenCraft(Product):
    def __init__(self, size, colour, craft_kind, description):
        self.size = size
        self.colour = colour
        self.craft_kind = craft_kind
        self.description = description