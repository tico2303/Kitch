from __future__ import print_function
from app import db
from app.V1.models import User, Location,Item
import json
from sqlalchemy.sql import exists
from locationservices import LocationService

class Dao(object):

    @staticmethod
    def create_user(data):
        raise NotImplementedError

    @staticmethod
    def create_item(self, data):
        raise NotImplementedError

    @staticmethod
    def get_items(data):
        raise NotImplementedError

    @staticmethod
    def create_location(data):
        raise NotImplementedError

    @staticmethod
    def get_locations_by_radius(data):
        raise NotImplementedError

    @staticmethod
    def get_users():
        raise NotImplementedError


# Mock data Class reads and writes data from json files in database dir
class File(Dao):
    def __init__(self):
        import os.path as path
        import sys
        self.dir = path.abspath(path.join(__file__,"../../.."))+"/database/"
        print("Data file directory: ", self.dir)

    def test_file_read(self):
        print("\n\n\n[~] Testing File Read\n\n\n")

        data = None
        with open(self.dir +"item.json",'r') as f:
            data = json.load(f)
        print("Data: ", data)

    @staticmethod
    def create_user(data):
        pass

# Database class that reads and writes to kitch.db in database dir
class Database(Dao):

    @staticmethod
    def create_user(data):
        fname = data.get('fname','')
        lname = data.get('lname','')
        email = data.get('email','')
        if db.session.query(User).filter_by(email=email).scalar() is not None:
            return {'ValidationError':'Email aready exists emails must be Unique'}
        user = User(fname=fname,lname=lname,email=email)
        db.session.add(user)
        db.session.commit()
        res = User.query.filter(User.id == user.id).first()
        return res

    @staticmethod
    def create_item(data):
        pass

    @staticmethod
    def get_items(data):
        return Item.query.all()

    @staticmethod
    def get_user(data):
        pass

    @staticmethod
    def get_users():
        return User.query.all()

    @staticmethod
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

    @staticmethod
    def get_locations():
        return Location.query.all()

    @staticmethod
    def get_location_by_radius(data):
        locs = db.session.query(Location).all()
        locs_list = [loc.address + " " + loc.city + ", " + loc.state + ", " + str(loc.zipcode) for loc in locs]
        loc_service = LocationService(data.get('source'),locs_list)
        res = loc_service.get_addr_by_radius(data.get('radius'))
        results = {"locations":[]}
        # TODO:
        #   consider moving all formating to LocationService class such that
        #   get_addr_by_radius returns properly formatted data
        for destinations in res:
            temp = {}
            for i,(k,v) in enumerate(destinations.items()):
                if k == "destination":
                    addr = {}
                    addr['address'] = v.get("fulladdress")
                    addr['city'] = v.get("city")
                    addr['state'] = v.get("state")
                    addr['zipcode'] = v.get("zipcode")
                    if not temp:
                        temp = {}
                    temp['source']=addr
                    temp['id'] = db.session.query(Location).filter_by(address=v.get("fulladdress")).first().id
                else:
                    if not temp:
                        temp = {}
                    temp['distance'] = v
                if (i+1)%2 == 0:
                    results['locations'].append(temp)
                    temp = {}
        return results

