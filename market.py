from repo import Repository

class Market(object):
    def __init__(self):
        self.repository = Repository("market.pkl")
        self.itemsOnMarket = self.repository.get_data()

    def _find_seller_by_item(self,item):
        for seller, itemList in self.itemsOnMarket.items():
            if item in itemList:
                return seller
        raise ValueError("Item: "+ str(item) + " not Found")

    def buy(self, buyer, item):
        buyer.cart.add(item)
        # FIX ME returns string not class instance
        seller = self._find_seller_by_item(item)
        seller.kitch.patron_orders[buyer]= item

    def offer(self,seller,item):
        if seller not in self.itemsOnMarket.keys():
            self.itemsOnMarket[seller] = []

        if item not in self.itemsOnMarket[seller]:
            self.itemsOnMarket[seller].append(item)
            self.repository.save_data(self.itemsOnMarket)

    def get_plates_for_sale(self):
        p = []
        for plateList in self.itemsOnMarket.values():
            p += plateList
        return p

