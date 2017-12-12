import pickle
import os

class Repository(object):
    def __init__(self,filename):
        self.filename = filename
        if filename not in os.listdir("."):
            os.system("touch "+filename )

    def get_data(self):
        try:
            return pickle.load(open(self.filename,'rb')) 
        except EOFError:
            return {}

    def save_data(self,data):
        pickle.dump(data,open(self.filename, 'wb'))




if __name__ == "__main__":
    r = Repository("market.pkl")
    print r.get_data()
