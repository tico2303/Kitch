import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy import create_engine, Sequence
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR,"/Kitch")
sys.path.insert(0,BASE_DIR)

dbfile = "sqlite:///kitch.db".format(DB_DIR)
print "DB_DIR: ", DB_DIR
print "BASE_DIR: ", BASE_DIR
print "dbfile: ", dbfile

Base = declarative_base()
###### Cart has Orders. Orders have Plates. Plates are made of Items
class Chef:
    pass
class Plate:
    pass
class Kitch:
    pass
#Item Many(Items) to 1(plate) relation
class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, Sequence('item_seq_id',start=1, increment=1), primary_key=True, unique=True)
    plate_id = Column(Integer, ForeignKey('plate.id'))
    name = Column(String(250), nullable=False)
    price = Column(Float)

#Plate Many(plates) to 1(kitch) 
class Plate(Base):
    __tablename__ = 'plate'
    id = Column(Integer, Sequence('plate_seq_id',start=1, increment=1),primary_key=True, unique=True)
    kitch_id = Column(Integer, ForeignKey('kitch.id'))
    items = relationship("Item", backref="plate")
    #name = Column(String(250), nullable=False)
    name = Column(String(250))
    is_public = Column(Boolean)

# Order Many(customers) to Many(kitchens)
# and   Many(kitchens) to Many(customers)
"""
class Order(Base):
    __tablename__= 'order'
    id = Column(Integer,primary_key=True,unique=True)
    buyer = relationship(Chef,backref="buyer", lazy="dynamic")
    seller_id = Column(Integer, ForeignKey('chef.id'))
    plates = relationship(Plate,backref="item",lazy="dynamic")
"""
# Kitch 1 to Many rel with Plate
class Kitch(Base):
    __tablename__ = 'kitch'
    id = Column(Integer,Sequence('plate_seq_id',start=1, increment=1),primary_key=True,unique=True)
    chef_id = Column(Integer, ForeignKey('chef.id'))
    plates =  relationship("Plate", backref="kitch")
    # patron_orders = relationship(Order,backref="patron_order", lazy="dynamic")

    def __repr__(self):
        return "Kitch(id=%s)"%(self.id)

class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer,Sequence('cart_seq_id',start=1, increment=1),primary_key=True)
    chef_id = Column(Integer, ForeignKey('chef.id'))
    #chef = None(backref from Chef)
    # orders = relationship(Order, backref="order", lazy="dynamic")

    def __repr__(self):
        return "Cart(id=%s)"%(self.id)

# Chef 1 to 1 relation with cart and kitch
class Chef(Base):
    __tablename__='chef'
    id = Column(Integer, Sequence('chef_seq_id',start=1, increment=1),primary_key=True )
    name = Column(String(250), nullable=False)
    cart = relationship(Cart, uselist=False, backref='chef')
    kitch =relationship(Kitch, uselist=False,backref='chef')

    def __repr__(self):
        if self.cart and self.kitch:
            return "Chef(name=%s, cartid=%s, kitchid=%s)"%(self.name, self.cart.id, self.kitch.id)
        elif self.cart and not self.kitch:
            return "Chef(name=%s, cartid=%s)"%(self.name, self.cart.id)
        elif self.kitch and not self.cart:
            return "Chef(name=%s, kitchid=%s)"%(self.name, self.kitch.id)
        else:
            return "Chef(name=%s)"%(self.name)

def setUpSession():
    engine = create_engine(dbfile)
    Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session

def populateChef_kitch_cart(sesh):
    chef1 = Chef(name="Chef Don Juan",cart=Cart(), kitch=Kitch())
    chef2 = Chef(name="Cheffy Chef",cart=Cart(), kitch=Kitch())
    chef3 = Chef(name="Netties",cart=Cart(), kitch=Kitch())
    chef4 = Chef(name="Lil Chef Xennie",cart=Cart(), kitch=Kitch())
    session.add(chef1)
    session.add(chef2)
    session.add(chef3)
    session.add(chef4)
    session.commit()

def createPlates(sesh):
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


if __name__ == "__main__":
    session = setUpSession()
    createPlates(session)
    populateChef_kitch_cart(session)

    xen = session.query(Chef).filter_by(name="Lil Chef Xennie").first()
    print xen
    burger_plate = session.query(Plate).filter_by(name="Burger Combo1").first()
    print burger_plate.name
    xen.kitch.plates.append(burger_plate)
    print xen.kitch.plates[0].name

