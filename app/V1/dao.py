from app import db
from app.V1.models import User, Location
import json
from sqlalchemy.sql import exists
from locationservices import LocationService

def create_user(data):
    fname = data.get('fname','')
    lname = data.get('lname','')
    email = data.get('email')
    print(db.session.query(User).filter_by(email=email).scalar())
    if db.session.query(User).filter_by(email=email).scalar() is not None:
        print("\n\nValidationError: Email aready exists\n\n\n")
        return {'ValidationError':'Email aready exists emails must be Unique'}
    # print("\nCreating User...\n\n")
    # print("info: ", fname, ",", lname, ",",email,"\n")
    user = User(fname=fname,lname=lname,email=email)
    db.session.add(user)
    db.session.commit()
    res = User.query.filter(User.id == user.id)
    print("\n\n\n res: ", res)
    j = res.serialize()
    print("jsoned: ",j)
    print("\n\n\n\n\n\n\n")
    return j

def create_item(data):
    pass 


def get_user(data):
    pass

def create_location(data):
    pass

def get_location(data):
    locs = db.session.query(Location).all()
    locs_list = [loc.address for loc in locs]
    loc_service = LocationService(data.get('source'),locs_list)

    res = loc_service.get_addr_by_radius(data.get('radius'))
    print(res)
    results = {"locations":[]}
    for destinations in res:
        for (source,dest), dist in destinations.items(): 
            temp = {}
            temp['source'] = dest
            temp['distance'] = dist
            temp['id'] = db.session.query(Location).filter_by(address=dest).first().id
            #temp[dest] = dist
            results['locations'].append(temp)
    print(results)
    return results

