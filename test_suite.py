from plate import *
from cart import Cart
from market import Market
from mykitch import MyKitch
from chef import Chef
import os


""" TEST #1 """
def testPlateNoItems():
    plate = Plate("Wings")
    assert plate.name == "Wings"
    assert plate.price == None
    assert plate.items == []

""" TEST #2 """
def testChefMakeOnePlate():
    bob = Chef("Bob")
    bob.kitch.add_plate(plate_name = "Wings")
    assert bob.kitch.get_plate("Wings").name == "Wings"

""" TEST #3 """
def testAddItemsToPlate():
    bob = Chef("Bob")
    bob.kitch.add_plate("Wings")
    bob.kitch.get_plate("Wings").add_item(Item(name="Boneless Wing",price=2.50))
    bob.kitch.get_plate("Wings").add_item(Item(name="Boneless Wing",price=2.50))
    bob.kitch.get_plate("Wings").set_price_by_items()
    assert ( len(bob.kitch.get_plate("Wings").items) == 2)
    assert ( bob.kitch.get_plate("Wings").get_price() == 5.00 )

""" TEST #4 """
def testPlateSetPrice():
    bob = Chef("Bobo")
    bob.kitch.add_plate("Wings")
    bob.kitch.get_plate("Wings").add_item(Item(name="Boneless Wing",price=2.50))
    bob.kitch.get_plate("Wings").add_item(Item(name="Boneless Wing",price=2.50))
    bob.kitch.get_plate("Wings").set_price_by_items()
    assert ( bob.kitch.get_plate("Wings").get_price() == 5.00 )
    bob.kitch.get_plate("Wings").set_price(10.53)
    assert ( bob.kitch.get_plate("Wings").get_price() == 10.53 )
    bob.kitch.get_plate("Wings").set_price_by_items()
    assert ( bob.kitch.get_plate("Wings").get_price() == 5.00 )

""" TEST #5 """
def testChefMultiplePlates():
    bob = Chef("bob1")
    bob.kitch.add_plate(plate_name = "Wings")
    bob.kitch.add_plate(plate_name = "Tacos")
    assert( bob.kitch.get_plate("Wings").name == "Wings")
    assert( bob.kitch.get_plate("Tacos").name == "Tacos")
    assert( len(bob.kitch.plates) == 2 )

def setUpPlatesToOrder():
    bob = Chef("bob2")
    bob.kitch.add_plate(plate_name = "Wings")
    bob.kitch.add_plate(plate_name = "Tacos")
    wingPlate = bob.kitch.get_plate("Wings")
    TacosPlate = bob.kitch.get_plate("Tacos")
    return wingPlate, TacosPlate

""" TEST #6 """
def testPatronCreateOrder():
    wingPlate,tacosPlate = setUpPlatesToOrder()
    patron = Chef("patron")
    patron.select_plate(wingPlate) 
    patron.select_plate(tacosPlate) 
    patron.place_order()


""" TEST #8 """
def testMarketOffer():
    patron = Chef("patron2")
    patron.kitch.add_plate(plate_name = "Wings")
    patron.kitch.add_plate(plate_name = "Tacos")
    patron.kitch.offer_on_market(patron.kitch.get_plate("Wings"))
    
    assert( patron.kitch.market.get_plates_for_sale()[0].name =="Wings" )

""" TEST #9 """
def testSamePlateOffer():
    carl = Chef("carl")
    fred = Chef("fred")
    carl.kitch.add_plate(plate_name = "Wings")
    carl.kitch.add_plate(plate_name = "Tacos")
    fred.kitch.add_plate(plate_name = "Wings")
    fred.kitch.add_plate(plate_name = "Tacos")
    market = Market()
    market.offer(carl, carl.kitch.get_plate("Wings"))
    market.offer(fred, fred.kitch.get_plate("Wings"))
    assert(market.itemsOnMarket[carl][0].name == "Wings")
    assert(market.itemsOnMarket[fred][0].name == "Wings")

def setUpMarket():
    carl = Chef("carlo")
    fred  = Chef("fredo")
    carl.kitch.add_plate(plate_name = "Wings")
    carl.kitch.add_plate(plate_name = "Tacos")
    fred.kitch.add_plate(plate_name = "Wings")
    fred.kitch.add_plate(plate_name = "Burritos")
    market = Market()
    market.offer(carl, carl.kitch.get_plate("Wings"))
    market.offer(carl, carl.kitch.get_plate("Tacos"))
    market.offer(fred, fred.kitch.get_plate("Wings"))
    market.offer(fred, fred.kitch.get_plate("Burritos"))
    return market, fred,carl 
   
""" TEST #10 """
def testMarketTransaction():
    market, fred, carl = setUpMarket()
    patron = Chef("patrano") 
    platesOnMarket = market.get_plates_for_sale()
    market.buy(patron,platesOnMarket[0] )
    printMarket(market)
    assert(patron.cart.get_order()[0].name == "Wings")
    assert( len(fred.kitch.patron_orders) == 1)
    assert( len(carl.kitch.patron_orders) == 0)

""" TEST #11 """
def testCartPrice():
    market, kitch1, kitch2 = setUpMarket()
    patron = Patron() 
    platesOnMarket = market.get_plates_for_sale()
    market.buy( patron,platesOnMarket[0] )
    assert(patron.cart.get_price() == 5)

def printMarket(market):
    print market.itemsOnMarket

os.system("rm market.pkl")

#1
testPlateNoItems()
#2
testChefMakeOnePlate()
#3
testAddItemsToPlate()
#4
testPlateSetPrice()
#5
testChefMultiplePlates()
#6
#testPatronCreateOrder()
#7
testMarketOffer()
#8
testSamePlateOffer()
#9

testMarketTransaction()
"""
testPatronCreateOrder()
#10
#11
testCartPrice()
"""

print "Passed!"





