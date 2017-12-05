from plate import Plate
from chef import *

def testPlateNoItems():
    plate = Plate("Wings")
    assert plate.name == "Wings"
    assert plate.price == None
    assert plate.items == None

def testChefMakeOnePlate():
    chefbob = Chef()
    chefbob.add_plate(plate_name = "Wings")
    chefbob.add_item(plate_name="Wings", item="Louisana Rub Wings")
    assert chefbob.get_plate("Wings").name == "Wings"
    assert chefbog.get_plate("Wings").get_item("Louisana Rub Wings").name == "Louisana Rub Wings"

def testChefMultiplePlates():
    chefbob = Chef()
    chefbob.add_plate(plate_name = "Wings")
    chefbob.add_plate(plate_name = "Tacos")
    assert( chefbob.get_plate("Wings").name == "Wings")
    assert( chefbob.get_plate("Tacos").name == "Tacos")
    assert( len(chefbob.plates) == 2 )

def testMarketBuy():
    pass    



testPlateNoItems()
testChefMakeOnePlate()
testChefMultiplePlates()

