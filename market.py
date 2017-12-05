
class Market(object):
    def __init__(self):
        self.itemsOnMarket = {}

    def _find_seller_by_item(self,item):
        for seller, itemList in self.itemsOnMarket.items():
            if item in itemList:
                return seller
        raise ValueError("Item: "+ str(item) + " not Found")

    def buy(self, buyer, item):
        buyer.cart.add_to_cart(item)
        seller = self._find_seller_by_item(item)
        
        seller.orders.append(item)

    def offer(self,seller,item):
        if seller not in self.itemsOnMarket.keys():
            self.itemsOnMarket[seller] = []
        if item not in self.itemsOnMarket[seller]:
            self.itemsOnMarket[seller].append(item)

    def get_plates_for_sale(self):
        p = []
        for plateList in self.itemsOnMarket.values():
            p += plateList
        return p

