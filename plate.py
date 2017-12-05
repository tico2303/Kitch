class Plate(object):
    def __init__(self, name=None):
        self.name = name
        self.price = None
        self.items = None

    def get_price(self):
        pass

    def add_item(self, item):
        self.items.append(item)

class Item(object):
    def __init__(self,name):
        self.name = name
        self.price = None

    def get_price(self):
        return self.price


