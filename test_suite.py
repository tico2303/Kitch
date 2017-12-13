from plate import *
from chef import *
from cart import Cart
from market import Market
from mykitch import MyKitch
from repo import MarketRepository
from models import *
from locationservices import LocationService

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
    assert ( len(chefbob.get_plate("Wings").items) == 2)

def testChefMultiplePlates():
    chefbob = Chef()
    chefbob.add_plate(plate_name = "Wings")
    chefbob.add_plate(plate_name = "Tacos")
    assert( chefbob.get_plate("Wings").name == "Wings")
    assert( chefbob.get_plate("Tacos").name == "Tacos")
    assert( len(chefbob.kitch.plates) == 2 )

def setUpPlatesToOrder():
    chefbob = Chef()
    chefbob.add_plate(plate_name = "Wings")
    chefbob.add_plate(plate_name = "Tacos")
    wingPlate = chefbob.get_plate("Wings")
    TacosPlate = chefbob.get_plate("Tacos")
    return wingPlate, TacosPlate


def testMarketOffer():
    chef = Chef()
    chef.add_plate(plate_name = "Wings")
    chef.add_plate(plate_name = "Tacos")
    chef.kitch.offer_on_market(chef.get_plate("Wings"))
    assert( chef.kitch.market.get_plates_for_sale()[0].name =="Wings" )

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

def testMarketTransaction():
    market, chef1, chef2 = setUpMarket()
    patron = Chef()
    platesOnMarket = market.get_plates_for_sale()
    market.buy(patron,platesOnMarket[0] )
    assert(patron.cart.get_order()[0].name == "Wings")
    assert( len(chef1.kitch.patron_orders) == 1)
    assert( len(chef2.kitch.patron_orders) == 0)

def testCartPrice():
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
    chef1 = Chef(name="Chef Don Juan",cart=Cart(), kitch=Kitch(),address=addr1)
    chef2 = Chef(name="Cheffy Chef",cart=Cart(), kitch=Kitch(),address=addr2)
    chef3 = Chef(name="Netties",cart=Cart(), kitch=Kitch(), address=addr3)
    chef4 = Chef(name="Lil Chef Xennie",cart=Cart(), kitch=Kitch(),address=addr4)
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
    return session.query(Chef).filter_by(name=chef_name).first()


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
testChefMakeOnePlate()
testChefMultiplePlates()
testMarketOffer()
testSamePlateOffer()
testMarketTransaction()
testAddItemsToPlate()
testCartPrice()
testRepo()
"""
sesh = setUpSession()
testLocation(sesh)
#create_Chef_kitch_cart(sesh)
#create_plates(sesh)
#add_plate_to_kitch(sesh)
#testDBModels()


print "Passed!"





