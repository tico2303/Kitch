from __future__ import print_function
from flask import jsonify, Blueprint
from flask import jsonify
from flask_restplus import Resource, Api, reqparse
# from app.V1.dao import Database
from app.V1.dao import File
from paymentservices import *
from searchservices import *
from locationservices import LocationService
from api_models import ApiModel

v1 = Blueprint('v1', __name__, url_prefix='/api/v1')
api = Api(v1, version='1.0', title="Kitch API", description="Documentation for Kitch RESTful API version 1.0")

apimodel = ApiModel(api)
Dao = File()
Dao.test_file_read()

#Eventually, this will allow us to use other packages with such as Stripe.
Payment = DaoPayment(Dao)

#Eventually, this will allow us to use other packages with such as Elastic Search.
Searcher = FileSearcher(Dao)

@api.route('/users')
class UsersList(Resource):

        @api.response(200, 'Success', apimodel.user_list_model())
        # api.doc defines parameters that can be entered in localhost-web interface (swagger)
        @api.doc(params={
                'id':'User Id',
                'email':'Email address',
                'fname':'First Name',
                'lname':"Last Name"})
        # ensures that the format of the get request follows the model
        @api.marshal_with(apimodel.user_list_format())
        def get(self):
            print("GET called on users endpoint")
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=str)
            args = parser.parse_args()

            if args['id'] is None:
                return {'ValueError':'Invalid userId'},500

            userlist = Dao.get_users()
            return userlist,200

        @api.expect(apimodel.user_list_format())
        def post(self):
            return Dao.create_user(api.payload)


#Give A User Id, Return All Items the Chef Has In the Database
@api.route('/user/items')
class UserItems(Resource):
        @api.response(200, 'Success', apimodel.user_items_model())
        @api.response(500, 'Failure')
        # api.doc defines parameters that can be entered in localhost-web interface (swagger)
        @api.doc(params={
                'id':'User Id'
                })
        # ensures that the format of the get request follows the model
        def get(self):
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=str)
            args = parser.parse_args()
            if args['id'] is None:
                return {'ValueError':'Invalid User ID'},500
            return Dao.get_items_from_seller(args)


#Add an Item to A Buyers Cart or Get a User Cart
@api.route('/cart')
class Cart(Resource):
        @api.response(200, 'Success', apimodel.cart_response_model())
        @api.response(500, 'Failure')
        #@api.marshal_with(apimodel.cart_get_model())
        @api.doc(params={
                'user_id':'User Id'
                })
        def get(self):
            parser = reqparse.RequestParser()
            parser.add_argument('user_id', type=str)
            args = parser.parse_args()
            if args['user_id'] is None:
                return {'ValueError':'Invalid User ID'},500
            return Dao.get_cart(args)

        @api.response(200, 'Success')
        @api.response(500, 'Failure')
        @api.expect(apimodel.cart_post_model())
        def post(self):
            return Dao.add_item_to_cart(api.payload)


@api.route('/locations')
class LocationList(Resource):
    @api.expect(apimodel.location_creation_format())
    def post(self):
        Dao.create_location(api.payload)
        return {'Success':'Location Created'},200

    @api.response(200,"Success",apimodel.locations_list())
    @api.marshal_with(apimodel.locations_list(),envelope="results")
    def get(self):
        locations = Dao.get_locations()
        return locations,200

@api.route('/location/radius')
class LocationList(Resource):
    @api.response(200, 'Success', apimodel.location_radius_response_list())
    @api.doc(params={"source":"Source addresss" ,
                     "radius":"Radius from source in miles"
                     })
    @api.marshal_with(apimodel.location_radius_response_format(),envelope="results")
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('source', type=str)
        parser.add_argument('radius', type=int)
        args = parser.parse_args()
        source_addr = args['source']
        if args['radius'] is None:
            args['radius'] = 10
        return Dao.get_users_by_location_radius(args)


@api.route('/item')
class ItemsList(Resource):
    @api.response(200, 'Success', apimodel.item_list_format())
    @api.response(500, 'Failure')
    @api.doc(params={
                    "item_id":"the id of the item you need"
                     })
    @api.marshal_with(apimodel.item_list_format())
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('itemid', type=str)
        args = parser.parse_args()
        return Dao.get_item(args)

    @api.expect(apimodel.item_list_format())
    @api.response(500, 'Failure', apimodel.item_failure_response())
    def post(self):
        return Dao.create_item(api.payload)

@api.route('/checkout')
class Checkout(Resource):
    @api.response(200, 'Success')
    @api.response(500, 'Failure')
    @api.expect(apimodel.payment_transaction_model())
    def post(self):
        return Payment.process_payment()

@api.route('/search/chef')
class Search(Resource):
    @api.response(200, 'Success', apimodel.search_chef_response_model())
    @api.response(500, 'Failure')
    @api.doc(params={
                        "user":"Enter the chef to search for"
                     })
   #@api.marshal_with(apimodel.search_chef_format())
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user', type=str)
        args = parser.parse_args()
        return Searcher.search_by_chef(args)

@api.route('/search/food_type')
class Search(Resource):
    @api.response(200, 'Success', apimodel.search_food_type_response_model())
    @api.response(500, 'Failure')
    @api.doc(params={
                        "Food Type":"Enter the food type to search for"
                     })
    #@api.marshal_with(apimodel.search_food_type_format())
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Food Type', type=str)
        args = parser.parse_args()
        return Searcher.search_by_food_type(args)

@api.route('/search/item')
class Search(Resource):
    @api.response(200, 'Success', apimodel.search_item_response_model())
    @api.response(500, 'Failure')
    @api.doc(params={
                        "item":"Enter the item to search for"
                     })
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('item', type=str)
        args = parser.parse_args()
        return Searcher.search_by_item(args)

@api.route('/search/location')
class Search(Resource):
    @api.response(200, 'Success', apimodel.search_location_response_model())
    @api.response(500, 'Failure')
    @api.doc(params={
                        "location":"Enter the location to search for"
                     })
    #@api.marshal_with(apimodel.search_food_type_format())
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('location', type=str)
        args = parser.parse_args()
        return Searcher.search_by_location(args)


#This Route will Create 1 order object provided neccessary information.
#Multiple Order Object May be in a Single Buyer's Order, Just call this function in a loop of the buyers cart
#TODO: Do we want a route to place create an order object for all items in a users cart.
@api.route('/order')
class Orders(Resource):
    @api.response(200, 'Success')
    @api.response(500, 'Failure')
    @api.doc(params={
                    "order_id":"The id of the order object.",
                    "buyer_id":"The id of the user placing the order object.",
                    "seller_id":"The id of the user selling the item",
                    "item_id":"The id of the item the user is making an order object for.",
                    "qnty":"The quantity of the item the user wants for the order object",
                    "is_done":"Order Completion identifier",
                    "is_in_progress":"Order In Progress identifier",
                    "is_delivery":"Specifies if this Order Is being Delivered",
                    "is_pickup":"Specifies if this Order is being picked up" 
                     })
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('buyer_id', type=int)
        parser.add_argument('seller_id', type=int)
        parser.add_argument('item_id', type=int)
        parser.add_argument('qnty', type=int)
        parser.add_argument('is_done', type=str)
        parser.add_argument('is_in_progress', type=str)
        parser.add_argument('is_delivery', type=str)
        parser.add_argument('is_pickup', type=str)
        args = parser.parse_args()
        if args['buyer_id'] is None:
            return {'Failure':'Invalid User ID'},500
        if args['seller_id'] is None:
            return {'Failure':'Invalid User ID'},500
        if args['item_id'] is None:
            return {'Failure':'Invalid Item ID'},500
        if args['qnty'] is None:
            return {'Failure':'Quantity Not Specified'},500
        return Dao.create_order(args)

    def get(self):
        pass




