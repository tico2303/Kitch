from plate import *
from cart import Cart

class User(object):
    pass

class Chef(object):
    def __init__(self):
        self.plates = {}
        self.orders = []
        self.cart = Cart()

    def add_plate(self, plate_name = None):
        self.plates[plate_name] = Plate(name = plate_name)

    def get_plate(self, plate_name):
        if plate_name in self.plates:
            return self.plates[plate_name]
        return None

    def get_recieved_orders(self):
        pass

