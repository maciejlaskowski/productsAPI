# Product aggregator microservice
Python 3 backend developer exercise
Create REST API JSON Python microservice


## Instructions
### **How to run the programme**
There are two ways to run the programme.
1. Create a **virtual environement** with the files provided.
  Once ready you can start it from the "src" folder with: _python -m app.MicroserviceAPI_
  To run the **tests** from the same folder execute: _python -m pytest -s_
 
2. Use the provided **Docker-compose** file.

### **How to use the programme**


The programme gives the following options:

**a) Change Offers microservice URL:**

PUT /api/v1.0/configure_offers
Headers: none
Request: none
{
“address”: <new URL>
}
Response:
200 OK
400 BAD REQUEST
{
  "error": "Wrong request"
}

**b) Get all products**

GET /products/api/v1.0/products/get_all_products
Headers: none
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

**c) Get one product**

GET /products/api/v1.0/products/get_product/

Headers: none
Request:
{
"id": <product id>
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

**d) Get all offers**

GET /products/api/v1.0/products/get_all_offers
Headers: none
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

**e) Add product**

POST /products/api/v1.0/products/add_product
Headers: none
Request: 
{
        "name": <product name>,
        "description": <product description>
}
Response:
200 OK
Product added
400 BAD REQUEST
{
  "error": "Wrong request"
}
  
**f) Update product**

PUT /products/api/v1.0/products/update_product
Headers: none
Request: 
{
        "id" : <product id>,
        "name": <product name>),
        "description": <product description>)
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

**f) Delete product**

DELETE /products/api/v1.0/products/delete_product
Headers: none
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
  
  
  

