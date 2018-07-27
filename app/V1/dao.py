from __future__ import print_function
import json
from locationservices import LocationService
import sys
# from sqlalchemy.sql import exists
# from flask_sqlalchemy import SQLAlchemy

class Serializer(object):

    def _data_to_obj(self,obj, data):
        for k in self._get_matching_keys(obj.__dict__, data):
            obj.__dict__[k] = data[k]

    def _get_matching_keys(self,dic1,dic2):
        return set(dic1.keys()).intersection(dic2.keys())

    def _print_all_attrs(self,obj):
        print(obj.__dict__)

#///////////// User  ////////////
class User(Serializer):

    def __init__(self,Accessor):
        self.id = None
        self.fname = None
        self.lname = None
        self.email = None
        self.accessor = Accessor

    def create_user(self,data):
        self._data_to_obj(self,data)
        if len(self.accessor.read(self, id=self.id)) != 0:
            return {"Failure":"User id not unique"}, 500
        return self.accessor.write(self)

    def get_users(self):
        return self.accessor.read(self)

    def get_user(self,data):
        self._data_to_obj(self,data)
        return self.accessor.read(self, id=self.id)

    def __str__(self):
        return "User"

#///////////// Item  ////////////
class Item(Serializer):

    def __init__(self,Accessor):
        self.item_id = None
        self.description = None
        self.ingredients = []
        self.price = None
        self.name = None
        self.seller = None
        self.lat = None
        self.lng = None
        self.img = None
        self.accessor = Accessor

    def create_item(self, data):
        self._data_to_obj(self,data)
        if len(self.accessor.read(self, item_id=self.item_id)) != 0:
            return {"Failure":"Itemid is not unique"}, 500
        self._set_lat_lng()
        return self.accessor.write(self)

    def get_items_from_seller(self,data):
        self._data_to_obj(self,data)
        return self.accessor.read(self,seller=data.get("id"))

    def get_item(self,data):
        self._data_to_obj(self,data)
        return self.accessor.read(self,item_id=self.item_id)

    def get_items(self):
        return self.accessor.read(self)

    def get_items_by_radius(self,data):
        #data has lat, lng and radius, number_of_results
        number_of_results = int(data.get("number_of_results",10))
        radius = int(data.get("radius",20))
        self._data_to_obj(self,data)
        items = self.accessor.read(self)
        results = []
        loc_serv = LocationService()
        for item in items:
            dist = int(loc_serv.get_lat_lng_distance(self.lat, self.lng, item.get("lat"), item.get("lng")))
            if dist <= radius:
                results.append(item)
        if number_of_results > len(results):
            return results
        return results[:number_of_results-1]


    def _set_lat_lng(self):
        if not self._is_lat_lng_set():
            location = self.accessor.read("Location",user_id=self.seller)
            if len(location) == 1:
                self.lat = location[0]["lat"]
                self.lng = location[0]["lng"]
            else:
                print("\n\n[!]Item::_set_lat_lng Error: lat and lng of Item could not be set\n\n")

    def _is_lat_lng_set(self):
        if self.lat == None or self.lng == None:
            return False
        return (self.lat != 0 or self.lng != 0)

    def __str__(self):
        return "Item"

#///////////// Location  ////////////
class Location(Serializer):

    def __init__(self,Accessor):
        self.id = None
        self.user_id = None
        self.lng = None
        self.lat = None
        self.street = None
        self.apt = None
        self.city = None
        self.state = None
        self.zip = None
        self.accessor = Accessor

    def create_location(self,data):
        loc_serv = LocationService()
        geometry = loc_serv.get_lat_lng(loc_serv.convert_to_address(data))
        data['lat'],data['lng'] = geometry['lat'],geometry['lng']
        self._data_to_obj(self,data)
        self.accessor.write(self)

    def get_users_by_location_radius(self,data):
        loc_serv = LocationService()
        geometry = loc_serv.get_lat_lng(data["source"])
        data['lat'],data['lng'] = geometry['lat'],geometry['lng']
        self._data_to_obj(self,data)
        locations = self.accessor.read(self)
        results = []
        radius = int(data.get("radius", "20"))
        for loc in locations:
            dist = loc_serv.get_lat_lng_distance(self.lat, self.lng, loc.get("lat"),loc.get("lng"))
            loc["distance"] = dist
            if dist <= radius:
                results.append(loc)
        return results

    def get_locations(self):
        return self.accessor.read(self)

    def __str__(self):
        return "Location"

#///////////// Order  ////////////
class Order(Serializer):

    def __init__(self, Accessor):
        self.seller_id = None
        self.is_done = None
        self.qnty = None
        self.item_id = None
        self.is_in_progress = None
        self.is_delivery = None
        self.buyer_id = None
        self.is_pickup = None
        self.accessor = Accessor

    def create_order(self,data):
        self._data_to_obj(self,data)
        return self.accessor.write(self)

    def __str__(self):
        return "Order"

#///////////// Cart  ////////////
class Cart(Serializer):
    def __init__(self, Accessor):
        self.user_id = None
        self.items = []
        self.total = None
        self.buyer_id = None
        self.accessor = Accessor

    def get_cart(self, data):
        self._data_to_obj(self,data)
        # items = self.accessor.read("Item")

    def add_item_to_cart(self, data):
        self._data_to_obj(self,data)
        self.accessor.write(self)

#///////////// Payment ////////////
class Payment(Serializer):
    def __init__(self, Accessor):
        self.accessor = Accessor

    def process_payment(self):
        return {"Success":"payment processed... implement process_paymen"},200

    def __str__(self):
        return "Payment"

#///////////// DAO ////////////
class Dao(object):
    def __init__(self,Accessor):
        self.dao = [User, Item, Location, Order, Payment, Cart]
        self.accessor = Accessor.connect()

    def __getattr__(self, method):
        try:
            for obj in self.dao:
                if hasattr(obj,method) and callable(getattr(obj,method)):
                    return getattr(obj(self.accessor),method)
        except AttributeError:
            print("AttributeError: method {} doesn't exit".format(method))

#///////////// Accessor ////////////
class Accessor(object):
    def __init__(self,type):
        self._type = type

    def connect(self,type=None):
        if type is not None:
            self._type = type
        if isinstance(self._type, File):
            return File()
        if isinstance(self._type, Database):
            return Database()

    def read(self, obj, **constraint):
        raise NotImplementedError

    def write(self, obj):
        raise NotImplementedError

#///////////// File ////////////
class File(Accessor):

    def __init__(self):
        import os.path as path
        import sys
        self.dir = path.abspath(path.join(__file__,"../../.."))+"/database/"
        self._type = self

    def read(self, obj, **constraint):
        data = None
        results = []
        try:
            with open(self.dir + str(obj).lower()+'.json','r') as f:
                data = json.load(f)
        except:
            print("Could not open file {} for reading".format(str(obj).lower()+'.json'))
            sys.exit()

        if constraint:
            for line in data:
                if self._is_meeting_constraint(line, constraint):
                    results.append(line)
        else:
            results = data

        return results

    def write(self, obj):
        existing_data = []
        try:
            with open(self.dir + str(obj).lower() +'.json', 'r') as f:
                existing_data = json.load(f)
            existing_data.append(self._remove_accessor(obj.__dict__))
        except ValueError:
            print("[!] File.write() ERROR: Could not open {} for reading ".format(file.lower()+".json"))
            return {"Failure":"{} not written, Error in read".format(str(obj))}, 500
        try:
            with open(self.dir +str(obj).lower() +'.json', 'w') as f:
                json.dump(existing_data,f, indent=2, separators={',',':'})
        except ValueError:
            print("[!] File.write() ERROR: Could not open {} for writing\n".format(file.lower()+".json"))
            return {"Failure":"{} not written, Error in write".format(str(obj))}, 500

        return {"Success":"{} was successfully written".format(str(obj))}, 200

    def _get_matching_keys(self,dic1,dic2):
        return set(dic1.keys()).intersection(dic2.keys())

    def _is_meeting_constraint(self,line, constraint):
        for k in self._get_matching_keys(line, constraint):
            if line[k] != constraint[k]:
                return False
        return True

    def _remove_accessor(self,obj):
        temp = {}
        for k, v in obj.items():
            if k.lower() != "accessor":
                temp[k] = v
        return temp

#///////////////// Database ///////////////
class Database(Accessor):
    def __init__(self):
        self._type = self

    def read(self, obj, **constraint):
        pass

    def write(self, obj):
        pass


if __name__ == "__main__":
    user2 = {"lname": "Straction", "id": "44", "fname": "Abby", "email": "Obscure@yahoo.com"}
    item2 = {"item_id": 777, "description": "added via new Dao interface!", "ingredients": ["cool 1"], "price": 99.99, "seller": 100, "name": "New Dao created item"}

    access = File()
    dao = Dao(access)
    print(dao.create_item(item2))
    print(dao.create_user(user2))
    print(dao.get_users())
    print(dao.get_item({"item_id":222}))
    print(dao.get_items())

