from random import *
from dao import File, Item

def make_items():
    f = File()
    names = [ "Deep Dish Boston Pizza", "Louisianna Wings", "Chili Jalapenos Nachos", "Wild Chicken", "Deep Fried Turkey", "Protein Packed Tuna", "Yellow Salmon", "Alfredo Cheese Pasta", "Over Medium Eggs and Bacon", "Fish Tacos", "Famous Dodger Hot Dogs", "Oatmeal", "Soup", "Fruit Bowl", "French Toast", "Burning Burger", "Lumber Jack Bash", "Lovers Omelette"]
    descriptions = [ "Good" + i + " with best ingredients around." for i in names ]
    ingredients = [ [word + "ingredient" for word in name] for name in names ]
    prices = [ "{0:.2f}".format(uniform(1,20)) for i in names]
    sellerid = sample(range(1, len(names)+1), len(names)) 
    itemid = sample(range(1, len(names)+1), len(names)) 
    lats = sample(range(20,200),len(names))
    lngs = sample(range(20,200),len(names))

    for i in range(len(name)):
            #f.write(Item(names[i],descriptions[i],ingredients[i],prices[i],sellerid[i],itemid[i],lats[i],lngs[i]))
            Item(Accessor=f,name=names[i],description=descriptions[i],ingredients=ingredients[i],price=prices[i],seller=sellerid[i],item_id=itemid[i],lat=lats[i],lng=lngs[i]).store()
    

if __name__ == '__main__':
    make_items()
