class Plate(object):
    def __init__(self, name=None):
        self.name = name
        self.price = None
        self.items = []

    def get_price(self):
        return self.price

    def calculate_price(self):
        price = 0
        for item in self.items:
            price += item.get_price()
        self.set_price(price)

    def add_item(self, item):
        self.items.append(item)

    def set_price(self, price):
        self.price = price

class Item(object):
    def __init__(self,name,price):
        self.name = name
        self.price = price

    def get_price(self):
        return self.price

if __name__ == "__main__":
    plate = Plate()
    plate.add_item(Item(name="firstItem", price=13))
    plate.add_item(Item(name="secondItem", price=6))
    # default price = price by item
    plate.set_price(plate.calculate_price())

    # set price = price that set
    price.set_price(10.00)

    # get_price = whichever one is set last
    price.get_price()


