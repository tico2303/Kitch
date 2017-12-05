class Cart(object):
    def __init__(self):
       self.order = [] 

    def add_to_cart(self,plate):
        self.order.append(plate)
    """
    def add_order_to_cart(self, plates):
        for plate in plates:
            self.order.append(plate)

    def add_item_to_cart(self, plate):
        self.order.append(plate)
    """

    def get_order(self):
        return self.order
