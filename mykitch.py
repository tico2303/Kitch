from plate import Plate
from market import Market

class MyKitch(object):
    def __init__(self,chef):
        self.patron_orders = {}
        self.plates = {}
        self.market = Market()
        self.chef = chef

    def add_plate(self,plate_name):
        self.plates[plate_name] = Plate(name=plate_name)

    def get_plate(self, plate_name):
        # Search class
        if plate_name in self.plates:
            return self.plates[plate_name]
        return None
     
    def offer_on_market(self,item):
        self.market.offer(self.chef,item) 
        
    def get_patron_orders(self):
        # use Search class
        pass

    def create_menu(self):
        pass
    
