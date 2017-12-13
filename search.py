
# search and filter
class Filter(object):

    @staticmethod
    def by_price():
        pass

    @staticmethod
    def by_location():
        pass


class Search(object):
    def __init__(self):
        self.filter = Filter()

    def _find_n_nearest_chefs(self,chef):
        pass

    def _find_plate_by_chef(self,plate):
        pass

    def find(self, *args, **kwargs):
        pass
