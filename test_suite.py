from plate import *
from chef import *
from cart import Cart
from patron import Patron
from market import Market

def testPlateNoItems():
    plate = Plate("Wings")
    assert plate.name == "Wings"
    assert plate.price == None
    assert plate.items == []

def testChefMakeOnePlate():
    chefbob = Chef()
    chefbob.add_plate(plate_name = "Wings")
    assert chefbob.get_plate("Wings").name == "Wings"

def testAddItemsToPlate():
    chefbob = Chef()
    chefbob.add_plate("Wings")
    chefbob.get_plate("Wings").add_item(Item(name="Boneless Wing",price=2.50))
    chefbob.get_plate("Wings").add_item(Item(name="Boneless Wing",price=2.50))
    assert ( len(chefbob.plates["Wings"].items) == 2)

def testChefMultiplePlates():
    chefbob = Chef()
    chefbob.add_plate(plate_name = "Wings")
    chefbob.add_plate(plate_name = "Tacos")
    assert( chefbob.get_plate("Wings").name == "Wings")
    assert( chefbob.get_plate("Tacos").name == "Tacos")
    assert( len(chefbob.plates) == 2 )

def setUpPlatesToOrder():
    chefbob = Chef()
    chefbob.add_plate(plate_name = "Wings")
    chefbob.add_plate(plate_name = "Tacos")
    wingPlate = chefbob.get_plate("Wings")
    TacosPlate = chefbob.get_plate("Tacos")
    return wingPlate, TacosPlate

def testPatronCreateOrder():
    wingPlate,tacosPlate = setUpPlatesToOrder()
    patron = Patron() 
    patron.select_plate(wingPlate) 
    patron.select_plate(tacosPlate) 
    patron.place_order()


def testMarketOffer():
    patron = Patron()
    chef = Chef()
    chef.add_plate(plate_name = "Wings")
    chef.add_plate(plate_name = "Tacos")
    market = Market()
    market.offer(chef, chef.get_plate("Wings"))
    assert( market.get_plates_for_sale()[0].name =="Wings" )

def testSamePlateOffer():
    chef1 = Chef()
    chef2 = Chef()
    chef1.add_plate(plate_name = "Wings")
    chef1.add_plate(plate_name = "Tacos")
    chef2.add_plate(plate_name = "Wings")
    chef2.add_plate(plate_name = "Tacos")
    market = Market()
    market.offer(chef1, chef1.get_plate("Wings"))
    market.offer(chef2, chef2.get_plate("Wings"))
    assert(market.itemsOnMarket[chef1][0].name == "Wings")
    assert(market.itemsOnMarket[chef2][0].name == "Wings")

def setUpMarket():
    chef1 = Chef()
    chef2 = Chef()
    chef1.add_plate(plate_name = "Wings")
    chef1.add_plate(plate_name = "Tacos")
    chef2.add_plate(plate_name = "Wings")
    chef2.add_plate(plate_name = "Burritos")
    market = Market()
    market.offer(chef1, chef1.get_plate("Wings"))
    market.offer(chef1, chef1.get_plate("Tacos"))
    market.offer(chef2, chef2.get_plate("Wings"))
    market.offer(chef2, chef2.get_plate("Burritos"))
    return market, chef1, chef2
    
def testMarketTransaction():
    market, chef1, chef2 = setUpMarket()
    patron = Patron() 
    platesOnMarket = market.get_plates_for_sale()
    market.buy(patron,platesOnMarket[0] )
    
    assert(patron.cart.get_order()[0].name == "Wings")
    assert( len(chef1.orders) == 1)
    assert( len(chef2.orders) == 0)

def testCartPrice():
    market, chef1, chef2 = setUpMarket()
    patron = Patron() 
    market.buy(patron,platesOnMarket[0] )
    assert(patron.cart.get_price() == 5)

testPlateNoItems()
testChefMakeOnePlate()
testChefMultiplePlates()
testMarketOffer()
testSamePlateOffer()
testMarketTransaction()
testAddItemsToPlate()


print "Passed!"





