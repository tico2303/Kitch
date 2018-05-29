from app import db

class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(100), unique=True, nullable=False)
        fname = db.Column(db.String(100), unique=False, nullable=True)
        lname = db.Column(db.String(100), unique=False, nullable=True)
        #One cart relationship
        cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
        location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
        # backref'ed columns
        # cart 
        # location
        # TODO
            # store_id
        def __init__(self, email, fname,lname):
            self.email = email
            self.fname = fname
            self.lname = lname

class Cart(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        total = db.Column(db.Float,)
        # many User's relationship
        users = db.relationship('User',backref='cart')
        # TODO:
            # many items to many carts

class Location(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        lat = db.Column(db.Float)
        lng = db.Column(db.Float)
        address = db.Column(db.String)
        city = db.Column(db.String)
        state = db.Column(db.String)
        zipcode = db.Column(db.Integer)
        #One location to many User's realtionship 
        users = db.relationship('User', backref='location')

class Store(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        isdelivery = db.Column(db.Boolean)
        ispickup = db.Column(db.Boolean)
        # TODO
            # inventory many items to many stores
            # orders many orders to many stores

class Item(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String)
        description = db.Column(db.String)
        price = db.Column(db.Float)
        qnty = db.Column(db.Integer)
        isdone = db.Column(db.Boolean)
        isinprogress = db.Column(db.Boolean)
        isdelivery = db.Column(db.Boolean)
        ispickup = db.Column(db.Boolean)

        # TODO:
            # one items many buyers
            # one item one seller 




