
from plate import *

class Chef(object):
    def __init__(self):
        self.plates = {}

    def add_plate(self, plate_name = None):
        self.plates[plate_name] = Plate(name = plate_name)

    def get_plate(self, plate_name):
        if plate_name in self.plates:
            return self.plates[plate_name].name
        return None
