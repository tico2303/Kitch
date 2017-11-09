#!/usr/bin/python
class Item(object):
    def __init__(self, name=None, description=None, images=None, price=None, ingredients=None,servingsize=None):
        self.name = name
        self.description = description
        self.images = images
        self.price = price
        self.servingsize = servingsize
        self.ingredients = ingredients

    def get(self, attr):
        return getattr(self, attr)

    def setName(self, name):
        self.name = name

    def setDescription(self, description):
        self.description = description

    def setPrice(self, price):
        self.price = price

    def setIngredients(self, ingredientList):
        self.ingredients = ingredientList

    def setServingSize(self, servingsize):
        self.servingsize = servingsize

class Plate(object):
    def __init__(self, name=None, description=None, images=None, price=None, itemList = []):
        self.name = name
        self.description = description
        self.images = images
        self.itemList = itemList
        self.__updatePrice(price)

    def get(self, attr):
        return getattr(self, attr)

    def setName(self, name):
        self.name = name

    def setDescription(self, description):
        self.description = description

    def setPrice(self, price):
        self.price = price

    def setPriceByItems(self):
        if len(self.itemList) ==0:
            print "Error: can't set price by item without items"
        else:
            self.price = self.__calculatePrice()

    def addItem(self, item):
        self.itemList.append(item)

    def addItems(self, itemList):
        self.itemList.extend(itemList)

    def __calculatePrice(self):
        newprice = 0
        if self.itemList is not None:
            for item in self.itemList:
                newprice += item.price
        else:
            newprice = 0
        return newprice

    def __updatePrice(self, newprice=None):
        if newprice == None:
            newprice = self.__calculatePrice()
        self.price = newprice

class Menu(object):
    def __init__(self, name=None, description=None, plateList = []):
        self.name = name
        self.description = description
        self.plates = plateList

    def get(self, attr):
        return getattr(self, attr)

    def setName(self, name):
        self.name = name

    def setDescription(self, description):
        self.description = description

    def addPlate(self, plate):
        self.plates.append(plate)

    def addPlates(self, plateList):
        for plate in plateList:
            self.plates.append(plate)

    def get(self, attr):
        return getattr(self,attr)




