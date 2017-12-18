from models import *
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
#get_name_pass("./data/names_pass.csv")
#get_addr_info("./data/us/or/portland_metro.csv")
make_users()
