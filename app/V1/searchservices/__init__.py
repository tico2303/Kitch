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

    def search_by_location():
        pass

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

    def search_by_chef():
        pass

    def search_by_food_type():
        pass
