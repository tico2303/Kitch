from plate import *
from cart import Cart
from market import Market
from mykitch import MyKitch

class Chef(object):
    def __init__(self,name):
        self.name = name
        self.cart = Cart(self)
        self.kitch = MyKitch(self)

    def get_recieved_orders(self):
        pass

    def add_to_cart(self,item):
        self.cart.add(self,item)

    def place_order(self):
        pass
