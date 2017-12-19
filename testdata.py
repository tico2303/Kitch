from models import *
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import random

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
                        phone_number="555 123 1234"
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

def make_orders():
    session = setUpSession() 

    for k in range(20):
        plates_to_order = []
        for i in range(5): 
            order = Order(contents = str(random.randint(1,5000)) +  " , " + str(random.randint(1,5000)), 
                    total = 5.00,
                    delivery_option = delivery_options[random.randint(0,len(delivery_options)-1)],
                    buyer_id = random.randint(1,20),
                    is_delivered = False
                    )
            print order.order_placed
            session.add(order)
    session.commit()



#get_name_pass("./data/names_pass.csv")
#get_addr_info("./data/us/or/portland_metro.csv")
make_users()
make_orders()





