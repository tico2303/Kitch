#!/usr/bin/python

#import sys
#sys.path.append("/home/roshi/code/chefapp/src/test")

from src.menu import Menu, MenuInfo

def Test_createMenu(plateList):
    menuInfo =MenuInfo("My First Menu", "This is my first menu",None)
    menu = Menu(menuInfo)
    for plate in plateList:
        menu.addPlate(plateList)
    return menu

def Test_Item():
    item1_info = Info()
    item1_info.setName("Rice")
    item1_info.setDescription("The rice from the indian hills")
    item1_info.setPrice(1.50)
    item1_info.setIngredients(["Rice", "salt"])
    item1_info.setServingSize(3)
    item1 = Item(item1_info) 

    plat1_info = Info()
    plat1_info.setName("Spanish Rice Plate with salmon")
    plat1_info.setPrice(20.00)



if __name__=="__main__":

    newMenu = Test_createMenu(["plate1", "plate2", "plate3", "plate4"])

    print("name: ", newMenu.menuInfo.name)
    print("description: ", newMenu.menuInfo.description)


