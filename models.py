import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy import create_engine, Sequence, Table
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR,"/Kitch")
sys.path.insert(0,BASE_DIR)
DBFILE = "sqlite:///kitch.db".format(DB_DIR)

# print "DB_DIR: ", DB_DIR
# print "BASE_DIR: ", BASE_DIR
# print "dbfile: ", DBFILE

Base = declarative_base()

class Chef:
    pass
class Plate:
    pass
class Kitch:
    pass
class Cart:
    pass
class Order:
    pass

#Item Many(Items) to 1(plate) relation
class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, Sequence('item_seq_id',start=1, increment=1), primary_key=True, unique=True)
    plate_id = Column(Integer, ForeignKey('plate.id'))
    name = Column(String(250), nullable=False)
    price = Column(Float)

# Order Many(customers) to Many(kitchens)
# and   Many(kitchens) to Many(customers)
"""
MarketOrder = Table("marketorder",
    Column("id",Integer,primary_key=True,unique=True),
    Column("buyer_id", Integer, ForeignKey('cart.id')),
    Column("seller_id",Integer, ForeignKey('kitch.id')))
"""
#Many(plates) to 1(kitch) 
class Plate(Base):
    __tablename__ = 'plate'
    id = Column(Integer, Sequence('plate_seq_id',start=1, increment=1),primary_key=True, unique=True)
    kitch_id = Column(Integer, ForeignKey('kitch.id'))
    items = relationship("Item", backref="plate")
    buyers = relationship("Chef",secondary="order",backref="plate")
    name = Column(String(250))
    is_public = Column(Boolean,default=False)

    def __repr__(self):
        return "Pate(name=%s, is_public=%s,items=%s)"%(self.name,
                self.is_public, [str(item.name)+"," for item in self.items])

class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer,Sequence('order_seq_id',start=1, increment=1),primary_key=True,unique=True)
    buyer_id = Column(Integer, ForeignKey('chef.id'))
    plate_id = Column(Integer, ForeignKey('plate.id'))

    is_delivered = Column(Boolean)
    #date

#1(kitch) to Many(Plate)
class Kitch(Base):
    __tablename__ = 'kitch'
    id = Column(Integer,Sequence('plate_seq_id',start=1, increment=1),primary_key=True,unique=True)
    chef_id = Column(Integer, ForeignKey('chef.id'))
    plates =  relationship("Plate", backref="kitch")
    #patron_orders = relationship(Order,backref="patron_order", lazy="dynamic")

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
    password = Column(String(250))
    email = Column(String(250) )
    address = Column(String(500))
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

if __name__ == "__main__":
    pass
    #session = setUpSession()
    #create_plates(session)
    #create_Chef_kitch_cart(session)
    #add_plate_to_kitch(session)

    #xen = find_chef_by_name(session,"Lil Chef Xennie")

    #Tests
    # create Chef with cart and kitch
    # create plate with items
    # kitch holds a list of plates
    # Cart holds a list of plates that make an order
    # Order: links buyers Cart to sellers plate in kitch


