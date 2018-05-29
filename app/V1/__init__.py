from flask import jsonify, Blueprint
from flask_restplus import Resource, Api, fields, reqparse

from app.V1.users_dao import create_user 
from app.V1.models import User
from .api_models import *

v1 = Blueprint('v1', __name__, url_prefix='/api/v1')
api = Api(v1, version='1.0', title="Kitch API", description="Documentation for Kitch RESTful API version 1.0")

user_list_format = api.model('User list format',{
                                "id":fields.String(description="id of User", required=True),
                                "email":fields.String(description="user's email", required=True),
                                "fname":fields.String(description="first name ", required=False),
                                "lname":fields.String(description="last name", required=False)
                                })

user_list_model = api.model('List of Users', {
    "user": fields.Nested(user_list_format)
    })

item_list_format = api.model('Item List format',{
                                "id":fields.String(description="id of Item", required=True),
                                "seller_id":fields.String(description="id of Item", required=True),


@api.route('/users')
class UsersList(Resource):

        @api.response(200, 'Success', user_list_model)
        # api.doc defines parameters that can be entered in localhost interface
        @api.doc(params={
                'id':'User Id',
                'email':'Email address',
                'fname':'Firstno.',
                'lname':"Last "})
        # ensures that the format of the get request follows the model
        @api.marshal_with(user_list_format)
        def get(self):
            print("GET called on users endpoint")
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=str)
            args = parser.parse_args()

            # print("\n\nargs: ", args, "\n\n")
            if args['id'] is None:
                return {'ValueError':'Invalid userId'},400

            #userlist = user_dao.get_user_list(args['userid'])
            # userlist = {"userid":"1234","email":"user1@gmail.com","fname":"Greatest","lname":"Ever"}
            userlist = User.query.all()
            return userlist,200

        @api.expect(user_list_model)
        def post(self):
            data = api.payload['user']
            print("[+] ", data)
            newuser = create_user(api.payload['user'])
            return newuser


@api.route('/item/<int:id>')
class ItemsList(Resource):
    

    def get(self):
        pass

    def post(self):
        pass

