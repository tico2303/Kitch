from plate import *
from cart import Cart
from market import Market
#from chef import Chef
import os
from models import *
from locationservices import LocationService


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
    chefbob = Chef()
    chefbob.add_plate("Wings")
    chefbob.get_plate("Wings").add_item(Item(name="Boneless Wing",price=2.50))
    chefbob.get_plate("Wings").add_item(Item(name="Boneless Wing",price=2.50))
    assert ( len(chefbob.get_plate("Wings").items) == 2)

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
    chef = Chef()
    chef.add_plate(plate_name = "Wings")
    chef.add_plate(plate_name = "Tacos")
    chef.kitch.offer_on_market(chef.get_plate("Wings"))
    assert( chef.kitch.market.get_plates_for_sale()[0].name =="Wings" )

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
    chef1 = Chef()
    chef2 = Chef()
    chef1.name = "Carl"
    chef2.name = "Fred"
    chef1.add_plate(plate_name = "Wings")
    chef1.add_plate(plate_name = "Tacos")
    chef2.add_plate(plate_name = "Boneless Wings")
    chef2.add_plate(plate_name = "Burritos")
    chef1.kitch.get_plate("Wings").add_item(Item(name="wing", price=2.50))
    chef1.kitch.get_plate("Wings").add_item(Item(name="wing2", price=2.50))
    chef1.kitch.get_plate("Tacos").add_item(Item(name="wing", price=2.50))
    chef2.kitch.get_plate("Boneless Wings").add_item(Item(name="beans", price=2.50))
    chef2.kitch.get_plate("Boneless Wings").add_item(Item(name="cheese", price=2.50))
    chef2.kitch.get_plate("Burritos").add_item(Item(name="cheese", price=2.50))
    market = Market()
    market.offer(chef1, chef1.get_plate("Wings"))
    market.offer(chef1, chef1.get_plate("Tacos"))
    market.offer(chef2, chef2.get_plate("Boneless Wings"))
    market.offer(chef2, chef2.get_plate("Burritos"))
    return market, chef1, chef2

""" TEST #11 """
def testCartPrice():
    market, kitch1, kitch2 = setUpMarket()
    patron = Patron() 
    platesOnMarket = market.get_plates_for_sale()
    market.buy( patron,platesOnMarket[0] )
    assert(patron.cart.get_price() == 5)

def printMarket(market):
    print market.itemsOnMarket
    market, chef1, chef2 = setUpMarket()
    platesOnMarket = market.get_plates_for_sale()
    patron = Chef()
    market.buy(patron,platesOnMarket[0] )
    assert(patron.cart.get_price() == 5)

########### DB Testing ###########
def setUpSession():
    engine = create_engine(DBFILE)
    Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session

def create_Chef_kitch_cart(session):
    addr1 = "3734 live oak creek way, Ontario, CA"
    addr2 = "1600 Amphitheatre Parkway, Mountain View, CA"
    addr3 = "900 University Ave, Riverside, CA"
    addr4 = "1133 W Blaine St, Riverside, CA"
    
    chef1 = Chef(name="Chef Don Juan",email="chef_don_juan@gmail.com",cart=Cart(), kitch=Kitch(),address=addr1)
    chef2 = Chef(name="Cheffy Chef",email="cheffy_chef@gmail.com",cart=Cart(), kitch=Kitch(),address=addr2)
    chef3 = Chef(name="Netties",email="netties@gmail.com",cart=Cart(), kitch=Kitch(), address=addr3)
    chef4 = Chef(name="Lil Chef Xennie", email="lil_chef_xennie@gmail.com",cart=Cart(), kitch=Kitch(),address=addr4)
    session.add(chef1)
    session.add(chef2)
    session.add(chef3)
    session.add(chef4)
    session.commit()

def create_plates(sesh):
    plate1 = Plate(name="Burger Combo1")
    p1 = Item(name="Burger", price=5)
    p2 = Item(name="Fries", price=2)
    plate1.items = [p1, p2]

    plate2 = Plate(name="Mexican Burrito")
    i1 = Item(name="Burrito", price=3)
    i2 = Item(name="Beans", price=1)
    i3 = Item(name="Rice", price=2)
    plate2.items = [i1,i2,i3]

    sesh.add(plate1)
    sesh.add(plate2)
    sesh.commit()

def add_plate_to_kitch(sesh):
    xen = sesh.query(Chef).filter_by(name="Lil Chef Xennie").first()
    netties = sesh.query(Chef).filter_by(name="Netties").first()
    cheffy = sesh.query(Chef).filter_by(name="Cheffy Chef").first()

    italian = Plate(name="Italian Dinner")
    p1 = Item(name="Spagetti", price=5)
    p2 = Item(name="Bread Sticks", price=2.50)
    p3 = Item(name="Meat Balls", price=3)
    p4 = Item(name="Soup", price=2.99)
    italian.items = [p1,p2,p3,p4]

    mexican = Plate(name="Wet Burrito")
    i1 = Item(name="Burrito", price=3)
    i2 = Item(name="Green Sauce", price=1)
    i3 = Item(name="Pico De Gallo", price=2)
    mexican.items = [i1,i2,i3]

    burger = Plate(name="Burger Combo2")
    b1 = Item(name="Burger", price=5)
    b2 = Item(name="Fries", price=2)
    burger.items = [b1, b2]

    thai = Plate(name="Pad Thai")
    t1 = Item(name="Thai Noodles", price=4.50)
    t2 = Item(name="Beef", price=5.0)
    thai.items = [t1, t2]

    netties.kitch.plates.append(italian)
    netties.kitch.plates.append(burger)
    cheffy.kitch.plates.append(mexican)
    xen.kitch.plates.append(thai)

    sesh.add(xen)
    sesh.add(netties)
    sesh.add(cheffy)
    sesh.commit()

def find_chef_by_name(sesh, chef_name):
    return sesh.query(Chef).filter_by(name=chef_name).first()

def test_order(sesh):
    chef = find_chef_by_name(sesh,"Cheffy Chef")
    seller = find_chef_by_name(sesh,"Netties")
    chef2 = find_chef_by_name(sesh,"Lil Chef Xennie")

    #print "Query result before adding order: ", sesh.query(Order).first()
    order = Order(buyer_id=chef.id,plate_id=seller.kitch.plates[0].id)
    print("seller.kitch.plates: ", seller.kitch.plates[0])
    #order.plates.append(seller.kitch.plates[0])
    order2 = Order(buyer_id=chef2.id, plate_id=seller.kitch.plates[0].id)
    sesh.add(order2)
    sesh.add(order)
    sesh.commit()
    print("First Row of Order:")
    print sesh.query(Order).all()

def testLocation(session):
    source_addr = session.query(Chef).filter_by(name="Netties").first().address
    dest1 = session.query(Chef).filter_by(name="Lil Chef Xennie").first().address
    dest2 = session.query(Chef).filter_by(name="Cheffy Chef").first().address
    print("source: ", source_addr)
    print("dest1: ", dest1)
    print("dest2: ", dest2)
    ls = LocationService(source_addr,[dest1,dest2])
    addr = ls.get_n_nearest_addr(1)
    print("addr", addr)
    print("Directions to nearest Chef is:\n ")
    print(ls.get_directions(addr))
"""
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
testAddItemsToPlate()
testCartPrice()
testRepo()
"""
sesh = setUpSession()
#testLocation(sesh)
create_Chef_kitch_cart(sesh)
create_plates(sesh)
add_plate_to_kitch(sesh)
test_order(sesh)
#testDBModels()

#testMarketTransaction()
"""
testPatronCreateOrder()
#10
#11
testCartPrice()
"""

print "Passed!"





