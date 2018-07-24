from flask_restplus import fields

class ApiModel(object):
    def __init__(self, api):
        self.api = api

    def user_list_format(self):
        return self.api.model('User list format',{
                                "id":fields.Integer(description="id of User", required=True),
                                "email":fields.String(description="user's email", required=True),
                                "fname":fields.String(description="first name ", required=False),
                                "lname":fields.String(description="last name", required=False)
                                })

    def user_list_model(self):
        return  self.api.model('List of Users', {
                                    "user": fields.Nested(self.user_list_format())
                                        })


    def item_list_format(self):
        return self.api.model('Item List format',{
                                "item_id":fields.Integer(description="id of the item"),
                                "seller":fields.Integer(description="sellers id", required=True),
                                "name":fields.String(description="Name of Item", required=True),
                                "price":fields.Float(description="Price of Item", required=False),
                                "description":fields.String(description="Description of the item", required=False),
                                "ingredients":fields.List(fields.String(description="list of ingredients",required=False))
                            })

    def item_failure_response(self):
        return self.api.model('Item Failure response',{
                                "Failure":fields.String(description="Reason for failure", required=False),
                            })

    def user_items_model(self):
        return  self.api.model('List of Items For A Given User', {
                                    "items": fields.Nested(self.item_list_format())
                                        })

    def cart_item_list_model(self):
        return self.api.model('A Cart Item With Quantity And Price', {
                "item_id":fields.Integer(description="Item Id", required=True),
                "qnty":fields.Integer(description="Quantity of item in Cart",required=True),
                "total":fields.Float(description="Total Price for Items", required=True)
            })

    def cart_get_model(self):
        return self.api.model('Cart format',{
                                "user_id":fields.Integer(description="id of the user", required=True)
                                })
        
    def cart_post_model(self):
        return self.api.model('Cart format',{
                                "buyer_id":fields.Integer(description="id of User that is buying the item", required=True),
                                "item": fields.Nested(self.cart_item_list_model(),required=True),
                                })

    def cart_response_model(self):
        return self.api.model('Cart format',{
                                "user_id":fields.Integer(description="id of the user", required=True),
                                "items":fields.List(fields.Nested(self.cart_item_list_model())),
                                "total":fields.Float(description="Total Price of Items In Cart")
                                })

    def location_creation_format(self):
        return self.api.model("Location Creation", {
                                "address":fields.String(description="Address of User", required=True),
                                "city":fields.String(description="City of User", required=True),
                                "state":fields.String(description="State of User", required=True),
                                "zip":fields.String(description="Zip Code of User", required=True)
                            })

    def location_radius_format(self):
        return self.api.model("Locations by Radius",{
                              "source":fields.String(description="Address of source (address,city,state)", required=True),
                              "radius":fields.Integer(description="Radius from source in miles",required="True")
                                })

    def location_radius_response_format(self):
        return self.api.model("Locations by Radius",{
                              "id":fields.Integer(description="id of the location", required=False),
                              "source":fields.String(description="Address of source (address,city,state)", required=True),
                              "distance":fields.Float(description="Radius from source in miles",required="True")
                                })
    def location_radius_response_list(self):
        return self.api.model("List of destinations and distance within specified radius",{
                                "locations":fields.Nested(self.location_radius_response_format())
                                })

    def locations_list(self):
        return self.api.model("List of all Locations",{
                              "id":fields.Integer(description="id of location", required=True),
                              "lat":fields.Float(description="Latitude of addres",required="False"),
                              "lng":fields.Float(description="Longitue of address",required="False"),
                              "address":fields.String(description="address", required=True),
                              "city":fields.String(description="city", required=True),
                              "state":fields.String(description="state", required=True),
                              "zipcode":fields.String(description="zipcode", required=False)
                                })

    #TODO: Add a TimeStamp field to this order object. 
    def orders_model(self):
        return self.api.model("Order Model",{
                              "id":fields.Integer(description="id of the location", required=False),
                              "item":fields.Nested(self.cart_item_list_model(),required=True),
                              "buyer_id":fields.Integer(description="ID of the user that is buying the order object", required=True),
                              "seller_id":fields.Integer(description="ID of the user that is selling the order object", required=True),
                              "is_done":fields.Bool(description="Order Completion identifier", required=True),
                              "is_in_progress":fields.Bool(description="Order In Progress identifier", required=True),
                              "is_delivery":fields.Bool(description="Specifies if this Order Is being Delivered", required=True),
                              "is_pickup":fields.Bool(description="Specifies if this Order is being picked up", required=True)
                                })

    def payment_transaction_model(self):
        return self.api.model("Payment Transaction Model",{
                              "id":fields.Integer(description="id of the location", required=False)
                                })

    def search_item_response_model(self):
        return self.api.model("Search Item Model",{
                                "items":fields.List(fields.Nested(self.item_list_format())),
                                })

    def search_chef_response_model(self):
        return self.api.model("Search Chef Model",{
                                "users":fields.List(fields.Nested(self.user_list_format())),
                                })

    def search_food_type_response_model(self):
        return self.api.model("Search Food Type Model",{
                                "items":fields.List(fields.Nested(self.item_list_format())),
                                })

    def search_location_response_model(self):
        return self.api.model("Search Food Type Model",{
                                "locations":fields.List(fields.Nested(self.locations_list())),
                                })



