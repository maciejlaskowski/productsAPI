# Product aggregator microservice
Python 3 backend developer exercise.

Create REST API JSON Python microservice.


## Instructions
### **How to run the programme**
There are three ways to run the programme.
1. Create a **virtual environement** with the files provided.

    Once ready you can start it with: _python -m app.MicroserviceAPI_
  
    To run the **tests** from the same folder execute: _python -m pytest -s_
 
2. Use the provided **Docker** and **Docker-compose** files.

3. Or use the **Heroku** url:

    https://products-api-heruko.herokuapp.com/


### **How to use the programme**

**Authentication:**

Use Bearer token: SuperAwesomeApi


The programme gives the following options:

**a) Add product**

POST /products/api/v1.0/products/add_product

Headers: Authorization: Bearer SuperAwesomeApi

Request: 

{

        "name": "<product name>",
        
        "description": "<product description>"
        
}

Response:

200 OK

Product added

400 BAD REQUEST

{

  "error": "Wrong request"
  
}

401 UNAUTHORIZED

Unauthorized Access

**b) Update product**

PUT /products/api/v1.0/products/update_product

Headers: Authorization: Bearer SuperAwesomeApi

Request: 

{

        "id" : <product id>,
        
        "name": "<product name>",
        
        "description": "<product description>")
        
}

Response:

200 OK

Product updated

400 BAD REQUEST

{

  "error": "Wrong request"
  
}

404 NOT FOUND

{

  "error": "Not found"
  
} 

401 UNAUTHORIZED

Unauthorized Access

**c) Delete product**

DELETE /products/api/v1.0/products/delete_product

Headers: Authorization: Bearer SuperAwesomeApi

Request: 

{

        "id" : <product id>
        
}

Response:

200 OK

Product deleted

400 BAD REQUEST

{

  "error": "Wrong request"
  
}

404 NOT FOUND

{

  "error": "Not found"
  
}

401 UNAUTHORIZED

Unauthorized Access

**d) Get one product**

GET /products/api/v1.0/products/get_product/

Headers: Authorization: Bearer SuperAwesomeApi

Request:

{

        "id" : <product id>
        
}

Response:

200 OK

[

  {
  
    "description": "<product description>",
    
    "id":<product id>,
    
    "name": "<product name>"
    
  }
  
]

400 BAD REQUEST

{

  "error": "Wrong request"
  
}

404 NOT FOUND

{

  "error": "Not found"
  
}

401 UNAUTHORIZED

Unauthorized Access

**e) Get all products**

GET /products/api/v1.0/products/get_all_products

Headers: Authorization: Bearer SuperAwesomeApi

Request: none

Response:

200 OK

[

  {
  
    "description": "<product description>",
    
    "id":<product id>,
    
    "name": "<product name>"
    
  },...
  
]

404 NOT FOUND

{

  "error": "Not found"
  
}

401 UNAUTHORIZED

Unauthorized Access

**f) Get offers for one product**

GET /products/api/v1.0/products/get_offers_one_product/

Headers: Authorization: Bearer SuperAwesomeApi

Request:

{

"id": <product id>
  
}

Response:

200 OK

[

  {
  
    "id": <offer id>,
    
    "items_in_stock": <stock>,
    
    "price": <price>,
    
    "product_id": <product id>
    
  }
  
]

400 BAD REQUEST

{

  "error": "Wrong request"
  
}

404 NOT FOUND

{

  "error": "Not found"
  
}

401 UNAUTHORIZED

Unauthorized Access

**g) Get all offers**

GET /products/api/v1.0/products/get_all_offers

Headers: Authorization: Bearer SuperAwesomeApi

Request: none

Response:

200 OK

[

  {
  
    "id": <offer id>,
    
    "items_in_stock": <stock>,
    
    "price": <price>,
    
    "product_id": <product id>
    
  },...
  
]

404 NOT FOUND

{

  "error": "Not found"
  
}

401 UNAUTHORIZED

Unauthorized Access

**h) Change Offers microservice URL:**

PUT /api/v1.0/configure_offers

Headers: Authorization: Bearer SuperAwesomeApi

Request: 

{

“address”: <new URL>
  
}

Response:

200 OK

400 BAD REQUEST

{

  "error": "Wrong request"
  
}

401 UNAUTHORIZED

Unauthorized Access
