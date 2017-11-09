#!/usr/bin/python
from src.menu import *

def Test_Menu():
    plateList = ["Plate1", "Plate2"]
    menu = Menu(name = "Mexican Food")
    menu.addPlates(plateList)

    print("name: ", menu.get("name"))
    if menu.get("name") == "Mexican Food" and len(menu.plates) > 0:
        print "Test Passed"

def Test_Item():
    item1 = Item()
    item1.setName("Rice")
    item1.setDescription("The rice from the indian hills")
    item1.setPrice(1.50)
    item1.setIngredients(["Rice", "salt"])
    item1.setServingSize(3)

    if item1.get("name") == "Rice": 
        print "Test Passed"

def Test_plate():
    Rice = Item(name="Rice", price=2.00)
    Tacos = Item(name="Tacos", price=4.50)
    plate = Plate()
    plate.setName("Rice and Tacos")
    plate.setDescription("Beef Street Tacos with Spanish Rice.")
    itemList = [Rice, Tacos]
    #plate.setPrice(10.01)
    #plate.addItems(itemList)
    plate.setPriceByItems()
    print plate.get("name")
    print plate.get("price")
    print plate.get("itemList")

    if plate.get("name") is not None:
        print "Test Passed"


if __name__=="__main__":

    Test_Item()
    Test_plate()
    Test_Menu()
