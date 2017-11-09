#!/usr/bin/python

class MenuInfo(object):
    def __init__(self, name=None, description=None, images=None):
        self.name = name
        self.description = description
        self.images = images

class Menu(object):
    def __init__(self, menuInfo):
        self.plates = []
        self.menuInfo = menuInfo

    def addPlate(self, plate):
        self.plates.append(plate)

    def addPlates(self, plateList):
        for plate in plateList:
            self.plates.append(plate)






