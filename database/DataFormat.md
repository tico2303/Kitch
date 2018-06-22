
## userObject:
    ```python
            {
            "id":uniqueIdentifier,
            "fname":"juan",
            "email":"juan1@gmail.com",
           "location":<locationObject>,
           "cart":<cartObject>,
           "store":<storeObject>
           }
    ```
## locationObject
    ```python
          {"userid":1234,
           "lng": 48.234,
            "lat": 2.3451,
            "address": "950 w. linden st.",
            "apt": 89,
            "city": "Riverside",
            "state": "CA",
            "zip": 92507,
           }

    ```
## storeObject
    ```python
           {"userid":1234,
           "orders":[{ "id":1, 
                       "item":"Sushi",
                       "price":10.99,
                       "qnty":1,
                       "buyer":<userObject>["id"],
                       "isdone":"False",
                       "isinprogress":"True",
                       "isdelivery":"True",
                       "ispickup":"False"
                       }],
            "isdelivery":"True",
            "ispickup":"False",
            "inventory":[{"name": "Sushi",
                          "price": 9.00,
                          "isavailable":"True"
                          },
                          {"name": "potatoes",
                           "price": 10.00,
                           "isavailable":"True"}
                           ]                    
            }

    ```
## cartObject
    ```python
           {"userid":1234,
           "items":[{"name":"Burrito",
                      "price":10.00,
                      "qnty":1,
                      "seller":<UserObject>["id"]
                    }],
            "total":10.00
            }

    ```
## itemObject
    ```python
        { "itemid":123,
          "name":"Burrito",
          "price":10.22,
          "seller":<UserObject>["id"],
          "description":"description of item",
          "ingredients":["rice","beans","tortilla"],
            }
    ```
