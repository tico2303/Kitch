import pickle

class Repo(object):
    def __init__(self,filename):
        self.filename = filename

    def getData(self):
        try:
            return pickle.load(open(self.filename,'rb')) 
        except EOFError:
            return []

    def saveData(self,data):
        pickle.dump(data,open(self.filename, 'wb'))



if __name__ == "__main__":
   pass 
