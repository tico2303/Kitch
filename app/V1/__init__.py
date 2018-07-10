from __future__ import print_function
from flask import jsonify, Blueprint
from flask import jsonify
from flask_restplus import Resource, Api, reqparse
# from app.V1.dao import Database
from app.V1.dao import File
from locationservices import LocationService
from api_models import ApiModel

v1 = Blueprint('v1', __name__, url_prefix='/api/v1')
api = Api(v1, version='1.0', title="Kitch API", description="Documentation for Kitch RESTful API version 1.0")

apimodel = ApiModel(api)
Dao = File()
Dao.test_file_read()

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
                return {'ValueError':'Invalid userId'},400

            userlist = Dao.get_users()
            return userlist,200

        @api.expect(apimodel.user_list_format())
        def post(self):
            Dao.create_user(api.payload)
            return {'Success':'User Created'},200

@api.route('/locations')
class LocationList(Resource):
    @api.expect(apimodel.location_creation_format())
    def post(self):
        create_location(api.payload)
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
        radius = args['radius']
        return get_locations_by_radius(args)['locations']



@api.route('/items')
class ItemsList(Resource):
    @api.response(200, 'Success', apimodel.item_list_format())
    @api.doc(params={
                     })
    @api.marshal_with(apimodel.item_list_format(),envelope="results")
    def get(self):
        return get_items("test")



