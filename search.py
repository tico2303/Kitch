from models import *
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
        self.session = self._setUpSession()

    def _setUpSession(self):
        engine = create_engine(DBFILE)
        Base.metadata.create_all(engine)
        Session = sessionmaker()
        Session.configure(bind=engine)
        session = Session()
        return session
    def find(self, obj, **kwargs):
        print kwargs
        print kwargs.keys()[0]

if __name__ == "__main__":
    s = Search()
    s.find("Chef",name="Cody")
