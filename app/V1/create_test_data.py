from app import db
from app.V1.models import User, Location, Item

id1=100
id2=101
id3=102
id4=103

def create_data():
    # add_locations()
    add_items()

def add_users():
    pass
def add_locations():
    loc1 = Location(id=id1,address="950 w. linden st.", city="Riverside", state="CA",zipcode=92507)
    loc2 = Location(id=id2,address="3734 live oak creek", city="Onartio", state="CA",zipcode=91761)
    loc3 = Location(id=id3,address="3321 Utah st.", city="Riverside", state="CA",zipcode=92507)
    loc4 = Location(id=id4,address="900 University ave.", city="Riverside", state="CA",zipcode=92521)

    #make sure we dont add dupes
    filter_q = {"id":id1,"id":id2,"id":id3,"id":id4}
    r1 = db.session.query(Location).filter_by(**filter_q).first()
    if not r1:
        db.session.add(loc1)
        db.session.add(loc2)
        db.session.add(loc3)
        db.session.add(loc4)
        db.session.commit()
        print("commited to database")
    else:
        res = db.session.query(Location).all()
        for loc in res:
            print(loc.id)
            print(loc.address)



def add_items():
    itm1 = Item(seller_id=id1, 
                name="Sushi",
                description="Spicy tuna Roll",
                price=6.99,
                qnty=5)

    itm2 = Item(seller_id=id2, 
                name="Tacos",
                description="bomb tacos",
                price=2.75,
                qnty=12)

    itm3 = Item(seller_id=id2, 
                name="Burritos",
                description="bomb Burritos",
                price=5.75,
                qnty=5)

    itm4 = Item(seller_id=id3, 
                name="Rice and Beans",
                description="White rice and black beans",
                price=6.24,
                qnty=2)

    db.session.add(itm1)
    db.session.add(itm2)
    db.session.add(itm3)
    db.session.commit()
    # res = db.session.query(Item).all()
    # for itm in res:
    #     print(itm.seller_id)
    #     print(itm.name)
    #     print(itm.price)
    #     print(itm.qnty)

