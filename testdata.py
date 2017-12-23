from models import *
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import random

PLATENAMES = ["linguinie", "Burger Combo", "My Amazing Plate", "Italian Dish", "Pizza", "Chicken Sandwitch","Soup","Steak and Rice","Jumbo","Sushi"]
ITEMS = {"linguinie":["noodles", "white sauce"], 
         "Burger Combo":["burger","fries"], 
         "My Amazing Plate":["fish","chips"],
         "Italian Dish":["spaghettie", "meat balls"],
         "Pizza":["pizza", "bread sticks"],
         "Chicken Sandwitch":["Chicken", "Sourdough bread"],
         "Soup":["chicken noodle soup"],
         "Steak and Rice":["NY steak", "brown rice"],
         "Jumbo":["cajon jumbo", "shrimp"],
         "Sushi":["california roll"]}

def make_plates():
    plateList =[]
    for i in range(len(PLATENAMES)):
        plt = Plate(name=PLATENAMES[i])
        items = ITEMS[PLATENAMES[i]]
        for j in range(len(items)):
            i1 = Item(name=items[j], price=random.randint(1,10))
            plt.items.append(i1)
        plateList.append(plt)
    return plateList

def add_plate_to_chefs(sesh,chef_List):
    PlateList = make_plates()
    length = min(len(chef_List),len(PlateList))
    for i in range(length-1):
        if PlateList[i] not in chef_List[i].plates:
            print "Adding plate: ", PlateList[i], " to ", chef_List[i]
            chef_List[i].plates.append(PlateList[i])
            sesh.add(chef_List[i])
    sesh.commit()

def get_name_pass(filename):
    li = []
    with open(filename,"r") as f:
        line = f.readline().split(",")
        lines = f.readlines()
        for line in lines:
            l = line.split(",")
            name = l[1]
            paswd = l[-1]
            li.append((name,paswd))
        f.close()
    return li

def get_addr_info(filename):
    li = []
    with open(filename,"r") as f:
        header = f.readline().split(",")
        lines = f.readlines()
        for line in lines:
            l = line.split(",")
            street_num = l[2]
            addr = l[3]
            city = l[5]
            zip_code = l[-3]
            city = "camas"
            street = street_num+" " + addr
            state = "oregon"
            li.append((street, city, state, zip_code))
        f.close()
    return li

def make_users():
    session = setUpSession()
    addr = get_addr_info("./data/us/or/portland_metro.csv")
    name_pas = get_name_pass("./data/names_pass.csv")
    userlist = []
    for i in range(20):
        name =name_pas[i][0].replace('"', "").strip()
        pas = name_pas[i][1].replace('"', "").strip()
        street = addr[i][0].strip("")
        city = addr[i][1].strip("")
        state = addr[i][2].strip("")
        zip_code = addr[i][3].strip("")
        pas = generate_password_hash(pas, method='sha256')
        print name
        print pas
        print type(name)
        print type(pas)
        print street
        print city
        print state
        print zip_code
        email = name + str(random.randint(1,999))+ "@gmail.com"
        user = Chef(name=name,
                        email=email,
                        password=pas,
                        street=street,
                        city=city,
                        state=state,
                        zip_code=zip_code,
                        apt_number="None",
                        phone_number="555 123 1234",
                        cart=Cart()
                        )
        print user
        session.add(user)
    session.commit()
    users = session.query(Chef).filter_by(name="Harry").first()
    print users.name+"."
    print users.password + "."

#COMMENT THESE OUT OR DELETE
"""
id = Column(Integer,Sequence('order_seq_id',start=1, increment=1),primary_key=True,unique=True)
contents = Column(ARRAY(Integer), ForeignKey('plate.id'))
order_placed = Column(Date)
total = Column(Float)
delivery_option = Column(String(250))
buyer_id = Column(Integer, ForeignKey('chef.id'))
is_delivered = Column(Boolean)
order_closed = Column(Date)
"""


delivery_options = ["pickup", "delivery", "meet"]
"""
def make_orders():
    session = setUpSession() 

    for k in range(20):
        plates_to_order = []
        for i in range(5): 
            order = Order( 
                    total = 5.00,
                    delivery_option = delivery_options[random.randint(0,len(delivery_options)-1)],
                    buyer_id = random.randint(1,20),
                    is_delivered = False
                    )
            session.add(order)
    session.commit()
"""


#get_name_pass("./data/names_pass.csv")
#get_addr_info("./data/us/or/portland_metro.csv")
session = setUpSession()
chefs = session.query(Chef).all()
add_plate_to_chefs(session,chefs)
make_users()
#make_orders()





