class Cart(object):
    def __init__(self):
       self.order = [] 

    def add_to_cart(self,item):
        self.order.append(item)

    def remove(self,item):
        if item in self.order:
            self.order.remove(item)

    def get_price(self):
        price = 0
        for item in self.order:
            price +=item.get_price()
        return price    

    def get_order(self):
        return self.order
