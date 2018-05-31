from flask_restplus import fields

class ApiModel(object):
    def __init__(self, api):
        self.api = api

    def user_list_format(self):
        return self.api.model('User list format',{
                                "id":fields.String(description="id of User", required=True),
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
                                "id":fields.String(description="id of Item", required=True),
                                "seller_id":fields.String(description="id Seller", required=True),
                                "name":fields.String(description="Name of Item", required=False),
                                "price":fields.String(description="Price of Item", required=False)
                            })

    def location_radius_format(self):
        return self.api.model("Locations by Radius",{
                              "source":fields.String(description="Address of source (address,city,state)", required=True),
                              "radius":fields.Integer(description="Radius from source in miles",required="True")
                                })

    def location_radius_response_format(self):
        return self.api.model("Locations by Radius",{
                              "id":fields.String(description="id of the location", required=False),
                              "source":fields.String(description="Address of source (address,city,state)", required=True),
                              "distance":fields.Float(description="Radius from source in miles",required="True")
                                })
    def location_radius_response_list(self):
        return self.api.model("List of destinations and distance within specified radius",{
                                "locations":fields.Nested(self.location_radius_response_format())
                                })

    def locations_list(self):
        return self.api.model("List of all Locations",{
                              "id":fields.String(description="id of location", required=True),
                              "lat":fields.Float(description="Latitude of addres",required="False"),
                              "lng":fields.Float(description="Longitue of address",required="False"),
                              "address":fields.String(description="address", required=True),
                              "city":fields.String(description="city", required=True),
                              "state":fields.String(description="state", required=True),
                              "zipcode":fields.String(description="zipcode", required=False)
                                })


