from app import db
from app.V1.models import User, Location,Item
import json
from sqlalchemy.sql import exists
from locationservices import LocationService

def create_user(data):
    fname = data.get('fname','')
    lname = data.get('lname','')
    email = data.get('email')
    print("The User Data Recieved: \n fname:",fname,"\n lname:", lname,"\n email:", email)
    print(db.session.query(User).filter_by(email=email).scalar())
    if db.session.query(User).filter_by(email=email).scalar() is not None:
        print("\n\nValidationError: Email aready exists\n\n\n")
        return {'ValidationError':'Email aready exists emails must be Unique'}
    # print("\nCreating User...\n\n")
    # print("info: ", fname, ",", lname, ",",email,"\n")
    user = User(fname=fname,lname=lname,email=email)
    db.session.add(user)
    db.session.commit()
    res = User.query.filter(User.email == user.email).first()
    if not res:
        raise ValueError("The Query Failed to Return A User.")
    print("The User Data Queried: \n fname:",res.fname,"\n lname:", res.lname,"\n email:", res.email, "\n id: ", res.id)

def create_item(data):
    pass 

def get_items(data):
    return Item.query.all()

def get_user(data):
    pass

def create_location(new_location):
    address = new_location['address']
    city = new_location['city']
    state = new_location['state']
    zipcode = new_location['zip']
    location = Location(address=address,city=city,state=state,zipcode=zipcode)
    db.session.add(location)
    db.session.commit()
    result = Location.query.filter(Location.id == location.id).first()
    print("result: ", result.city)


def get_location(data):
    locs = db.session.query(Location).all()
    locs_list = [loc.address + " " + loc.city + ", " + loc.state + ", " + str(loc.zipcode) for loc in locs]
    loc_service = LocationService(data.get('source'),locs_list)

    res = loc_service.get_addr_by_radius(data.get('radius'))
    # print(res)
    results = {"locations":[]}
    for destinations in res:
        temp = {}
        for i,(k,v) in enumerate(destinations.items()):
            if k == "destination":
                print("well its the destination")
                addr = {}
                addr['address'] = v.get("fulladdress")
                addr['city'] = v.get("city")
                addr['state'] = v.get("state")
                addr['zipcode'] = v.get("zipcode")
                if not temp:
                    print("no temp\n")
                    temp = {}
                temp['source']=addr
                temp['id'] = db.session.query(Location).filter_by(address=v.get("fulladdress")).first().id

            else:
                print("tuple : ", v)
                if not temp:
                    print("no temp\n")
                    temp = {}
                temp['distance'] = v
            if (i+1)%2 == 0:
                results['locations'].append(temp)
                temp = {}
    # print(results)
    return results

