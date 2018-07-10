
## userObject:
```python
{
    "id":uniqueIdentifier,
    "fname":"juan",
    "lname":"gomez",
    "image":"url/to/image.png,
    "email":"juan1@gmail.com",
    "location":<locationObject>["id"],
    "cart":<cartObject>["id"],
    "store":<storeObject>["id"]
}
```
## locationObject
```python
{
    "userid":<userObject>["id"],
    "lng": 48.234,
    "lat": 2.3451,
    "street": "950 w. linden st.",
    "apt": 89,
    "city": "Riverside",
    "state": "CA",
    "zip": 92507,
}

```
## storeObject
```python
{
"userid":1234,
"orders":[
            <orderObject>1,
            <orderObject>2
          ],
"isdelivery":"True",
"ispickup":"False",
"inventory":[
            <inventoryObject>1,
            <inventoryObject>2
               ]                    
}

```
## inventoryObject
```python
{
"id":99,
"item":<itemObject>["id"],
"isavailable":"True",
"isvisible":"True",
"qnty":10
}


```


## orderObject
```python
{ 
"id":1, 
"item":<itemObject>["id"],
"price":5.00,
"timestamp":<timeObject>,
"qnty":1,
"buyer":<userObject>["id"],
"isdone":"False",
"isinprogress":"True",
"isdelivery":"True",
"ispickup":"False"
}
# should an orderObject have an explicit price?
# this would avoid a change in item price effecting the 
# agreed upon price.
```

## timeObject
```python
{
    "id":444,
    "orderid":1,
    "date":"12/22/2018",
    "time":"13:22:44",
    "timezone":"PST"
}
```


## cartObject
```python
{
"userid":1234,
"items":[
          {
          "item":<itemObject>['id'],
          "qnty":1,
          }
         ],
"total":10.00
}

```
## itemObject
```python
{
"itemid":123,
"name":"Burrito",
"price":10.22,
"seller":<UserObject>["id"],
"description":"description of item",
"ingredients":[
                "rice",
                "beans",
                "tortilla"
                ]
}
```
