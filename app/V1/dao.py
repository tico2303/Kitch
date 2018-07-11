from __future__ import print_function
from app import db
from app.V1.models import User, Location,Item
import json
from sqlalchemy.sql import exists
from locationservices import LocationService

class Dao(object):

    def create_user(self,data):
        raise NotImplementedError

    def create_item(self, data):
        raise NotImplementedError

    def add_item_to_cart(data):
        raise NotImplementedError

    def get_item(self,data):
        raise NotImplementedError

    def create_location(self,data):
        raise NotImplementedError

    def get_locations_by_radius(self,data):
        raise NotImplementedError

    def get_users(self):
        raise NotImplementedError

# Mock data Class reads and writes data from json files in database dir
class File(Dao):
    def __init__(self):
        import os.path as path
        import sys
        self.dir = path.abspath(path.join(__file__,"../../.."))+"/database/"
        print("Data file directory: ", self.dir)

    def test_file_read(self):
        # print("\n\n\n[~] Testing File Read\n\n\n")
        # data = None
        # with open(self.dir +"item.json",'r') as f:
            # data = json.load(f)
        #print("Data: ", data)
        pass

    def create_user(self,data):
        try:
            with open(self.dir +"user.json",'a') as f:
                json.dump(data,f)
            return {'Success':'User Created'},200
        except:
            return {'Failure':'Create User Unsuccessful In Dao - File'},400

    def add_item_to_cart(self,data):
        try:
            item_list = []
            with open(self.dir +"cart.json",'r') as f:
                try:
                    item_list = json.load(f)
                except ValueError as e:
                    print("Warning - Cart Was Maybe Empty printing error: ", e)
                    print("Proceeding With An Empty Cart List")
                    item_list = []
                print("Item List: \n", item_list)
            item_list.append(data)
            with open(self.dir +"cart.json",'w') as f:
                json.dump(item_list,f)
            return {'Success':'Added Item To Cart'},200
        except:
            return {'Failure':'Unable to add to Item to Cart In Dao - File'},400

    def get_cart(self,data):
        try:
            cart = {}
            cart['user_id'] = data['user_id']
            cart['items'] = []
            cart['total'] = 0
            items = []
            print("Data: \n", data)
            with open(self.dir +"item.json",'r') as f2:
                items = json.load(f2)
            with open(self.dir +"cart.json",'r') as f:
                carts = json.load(f)
                for cart_item in carts:
                    if cart_item['buyer_id'] == data['user_id']:
                        cart['items'].append(cart_item)
                        for item in items:
                            if item['itemid'] == cart_item['item']['item_id']:
                                cart['total'] += float(cart_item['item']['qnty']) * item['price']
            return cart,200
        except:
            return {'Failure':'Unable to add to Item to Cart In Dao - File'},400

    def get_items(self,data):
        try:
            seller_items = {}
            seller_items["items"] = []
            with open(self.dir +"item.json",'r') as f:
                all_items = json.load(f)
                print("All Items:", all_items)
                for item in all_items:
                    print("Current Item: ", item)
                    if int(item['seller']) == int(data['id']):
                        seller_items["items"].append(item)
                        print("Item Added To List")
            print("Seller Items:", seller_items)
            return seller_items,200
        except ValueError as e:
            print(e)
        except TypeError as e:
            print(e)
        except: 
            pass
        return {'Failure':'Unable To Retrieve User Item List In Dao - File'},400


    def get_item(self,data):
        itemslist = []
        try:
            with open(self.dir +"item.json",'r') as f:
                itemslist = json.load(f)
            itemid = data.get("itemid")
            for item in itemslist:
                if int(item.get("itemid")) == int(itemid):
                    return item, 200
            return {"Failure":"item with id {} not found".format(itemid)},400
        except:
            return {"Failure":"Unable to Get items"}, 400

    def create_item(self, data):
        try:
            itemsList = []
            with open(self.dir + "item.json",'r') as f:
                try:
                    itemsList = json.load(f)
                except ValueError:
                    print("[!] Warning item.json is empty")
                    itemsList = []
                for item in itemsList:
                    if data.get("itemid")  == item.get("itemid"):
                        # print("[!] Error: itemid NOT UNIQUE")
                        return {"Failure":"Itemid not unique"}, 400

            itemsList.append(data)
            with open(self.dir + "item.json",'w') as f:
                json.dump(itemsList,f)
            return data, 200
        except:
            return {"Failure":"Read/write failure"}, 400

# Database class that reads and writes to kitch.db in database dir
class Database(Dao):

    def create_user(self,data):
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

    def add_item_to_cart(data):
        pass

    def create_item(self,data):
        pass


    def get_items(self,data):
        return Item.query.all()


    def get_user(self,data):
        pass


    def get_users(self):
        return User.query.all()


    def create_location(self,new_location):
        address = new_location['address']
        city = new_location['city']
        state = new_location['state']
        zipcode = new_location['zip']
        location = Location(address=address,city=city,state=state,zipcode=zipcode)
        db.session.add(location)
        db.session.commit()
        result = Location.query.filter(Location.id == location.id).first()
        print("result: ", result.city)

    def get_locations(self,):
        return Location.query.all()


    def get_location_by_radius(self,data):
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

