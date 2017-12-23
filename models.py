import os
import datetime
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, Date, ARRAY, func, DateTime
from sqlalchemy import create_engine, Sequence, Table
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR,"/Kitch")
sys.path.insert(0,BASE_DIR)
DBFILE = "sqlite:///kitch.db".format(DB_DIR)

def setUpSession():
    engine = create_engine(DBFILE)
    Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session

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

items = Table('items',
                Base.metadata,
                Column('item_id', Integer, ForeignKey('item.id')),
                Column('plate_id', Integer, ForeignKey('plate.id'))
                )

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, Sequence('item_seq_id',start=1, increment=1), primary_key=True, unique=True)
    plate_id = Column(Integer, ForeignKey('plate.id'))
    name = Column(String(250), nullable=False)
    price = Column(Float)
    plates = relationship('Plate', secondary=items, backref='items') 


#Many(plates) to 1(kitch) 
class Plate(Base):
    __tablename__ = 'plate'
    id = Column(Integer, Sequence('plate_seq_id',start=1, increment=1),primary_key=True, unique=True)
    chef_id = Column(Integer, ForeignKey('chef.id'))
    name = Column(String(250))
    is_public = Column(Boolean,default=False)
    orders = relationship("Order", backref="plate")

    #### BackRefs ###
    # items

    def __repr__(self):
        return "Plate(name=%s, is_public=%s,items=%s)"%(self.name,
                self.is_public, [str(item.name)+"," for item in self.items])

order_contents = Table('order_contents', 
                    Base.metadata,
                    Column('order_id', Integer, ForeignKey('order.id')),
                    Column('plate_id', Integer, ForeignKey('plate.id'))
                    )

market_order = Table('market_order', 
                    Base.metadata,
                    Column('chef_id', Integer, ForeignKey('chef.id')),
                    Column('order_id', Integer, ForeignKey('order.id'))
                    )


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer,Sequence('order_seq_id',start=1, increment=1),primary_key=True,unique=True)
    order_placed = Column(Date, default=datetime.datetime.now())
    total = Column(Float)
    delivery_option = Column(String(250))
    is_delivered = Column(Boolean)
    order_closed = Column(Date, default=datetime.datetime.now())
    plate_id = Column(Integer, ForeignKey('plate.id'))
    buyer_id = Column(Integer, ForeignKey('chef.id'))

    ### BackRefs ###
    # chef
    # plate


    def __repr__(self):
        return "Order(id=%s, order_placed=%s, total=%s, delivery_option=%s, buyer_id=%s, plate_id=%s, is_delivered=%s, order_closed=%s)"%(self.id, self.order_placed, self.total, self.delivery_option, self.buyer_id, self.plate_id, self.is_delivered, self.order_closed)
    #date

"""
#1(kitch) to Many(Plate)
class Kitch(Base):
    __tablename__ = 'kitch'
    id = Column(Integer,Sequence('plate_seq_id',start=1, increment=1),primary_key=True,unique=True)
    chef_id = Column(Integer, ForeignKey('chef.id'))
    plates =  relationship("Plate", backref="kitch")

    ### BackRef ###
    # chef

    def __repr__(self):
        return "Kitch(id=%s)"%(self.id)
"""
cart_contents = Table('cart_contents', 
                    Base.metadata,
                    Column('cart_id', Integer, ForeignKey('cart.id')),
                    Column('plate_id', Integer, ForeignKey('plate.id'))
                    )
class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer,Sequence('cart_seq_id',start=1, increment=1),primary_key=True)
    chef_id = Column(Integer, ForeignKey('chef.id'))
    plates = relationship('Plate', secondary = cart_contents, backref='cart')
    ### BackRef ###
    # chef

    def __repr__(self):
        return "Cart(id=%s)"%(self.id)

# Chef 1 to 1 relation with cart and kitch
class Chef(UserMixin,Base):
    __tablename__='chef'
    id = Column(Integer, Sequence('chef_seq_id',start=1, increment=1),primary_key=True )
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True )
    password = Column(String(250),nullable=False)
    street = Column(String(500), nullable=False)
    city = Column(String(500), nullable=False)
    state = Column(String(500), nullable=False)
    zip_code = Column(String(500), nullable=False)
    apt_number = Column(String(500)),
    phone_number = Column(String(500))
    plates =relationship(Plate, backref='chef')
    orders = relationship(Order,backref='buyer')
    cart = relationship('Cart',uselist=False, backref='chef')
    ### BackRef ###
    

    def __repr__(self):
            return "Chef(name=%s, email=%s)"%(self.name, self.email)

if __name__ == "__main__":
    pass


