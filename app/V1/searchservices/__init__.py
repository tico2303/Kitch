from app.V1.dao import File

class SearchContract(object):
    def search_by_location():
        pass

    def search_by_item():
        pass

    def search_by_chef():
        pass

    def search_by_food_type():
        pass

class FileSearcher(SearchContract):
    def __init__(self,DaoObj):
        self.Dao = DaoObj

    def search_by_location(self,data):
        search_location = data['location']
        locations = self.Dao.get_locations()
        print("All Locations: \n", locations)
        search_results = []
        for location in locations:
            city = location['city']
            street = location['street']
            state = location['state']
            zipcode = location['zip']

            if search_location.lower() in city.lower():
                search_results.append(location)
            elif search_location.lower() in street.lower():
                search_results.append(location)
            elif search_location.lower() in state.lower():
                search_results.append(location)
            elif str(search_location).lower() in str(zipcode).lower():
                search_results.append(location)
        return search_results

    def search_by_item(self,data):
        search_item = data['item']
        items = self.Dao.get_items()
        print("All Items: \n", items)
        search_results = []
        for item in items:
            name = item['name']
            if search_item.lower() in name.lower():
                search_results.append(item)
        return search_results

    def search_by_chef(self,data):
        print("Data: :", data)
        search_chef = data['user']
        users = self.Dao.get_users()
        print("All Users: \n", users)
        search_results = []
        for user in users:
            name = user['fname'] + user['lname']
            if search_chef.lower() in name.lower():
                search_results.append(user)
        return search_results

    #TODO: This function now only looks at the description for its type. 
    #       Maybe an additional field may be added to item in the future for 
    #       this function to parse for search purposes as well.
    def search_by_food_type(self,data):
        search_food_type = data['Food Type']
        items = self.Dao.get_items()
        print("All Items: \n", items)
        search_results = []
        for item in items:
            description = item['description']
            if search_food_type.lower() in description.lower():
                search_results.append(item)
        return search_results



