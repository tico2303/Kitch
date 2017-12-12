from market import Market

class Cart(object):
    def __init__(self,chef):
       self.order = [] 
       self.market = Market()
       self.chef = chef

    def add(self,item):
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
    
    def purchase(self):
        for item in self.order:
            market.buy(self.chef,item) 
