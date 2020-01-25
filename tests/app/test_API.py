# Test Microservice API
import pytest

header = {"Authorization": "Bearer SuperAwesomeApi"}

def test_no_token_access(client):
    response = client.get("/products/api/v1.0/products/get_all_products")
    
    assert response.status_code == 401

def test_get_all_products_no_products(client):
    response = client.get("/products/api/v1.0/products/get_all_products", headers = header)
    
    assert response.status_code == 404

def test_get_one_products_no_products(client):
    request_payload = {"id": 1}
    response = client.get('/products/api/v1.0/products/get_product/', json = request_payload,  headers = header)

    assert response.status_code == 404

def test_get_all_offers_no_offers(client):
    response = client.get('/products/api/v1.0/products/get_all_offers', headers = header)

    assert response.status_code == 404

def get_offers_for_one_product_no_products(client):
    request_payload = {"id": 1}
    response = client.get("/products/api/v1.0/products/get_offers_one_products", json = request_payload,  headers = header)

    assert response.status_code == 404

def test_add_product(client):
    # No product name in request
    request_payload = {"description": "test description"}
    response = client.post("/products/api/v1.0/products/add_product", json=request_payload,  headers = header)
    result = response.get_json()

    assert response.status_code == 400

    # Product name wrong format
    request_payload = {"name": 000, "description": "test description"}
    response = client.post("/products/api/v1.0/products/add_product", json=request_payload,  headers = header)
    result = response.get_json()

    assert response.status_code == 400

    # Description wrong format
    request_payload = {"name": "test product", "description": 000}
    response = client.post("/products/api/v1.0/products/add_product", json=request_payload,  headers = header)
    result = response.get_json()

    assert response.status_code == 400

    # Add correct product
    request_payload = {"name": "test product", "description": "test description"}
    response = client.post("/products/api/v1.0/products/add_product", json=request_payload,  headers = header)
    result = response.get_json()

    assert response.status_code == 200

def test_update_product(client):
    # No product id in request
    request_payload = {"description": "test description"}
    response = client.put("/products/api/v1.0/products/update_product", json=request_payload,  headers = header)
    result = response.get_json()

    assert response.status_code == 400

    # Name in wrong format
    request_payload = {"name": 000}
    response = client.put("/products/api/v1.0/products/update_product", json=request_payload,  headers = header)
    result = response.get_json()

    assert response.status_code == 400

    # Description in wrong format
    request_payload = {"description": 000}
    response = client.put("/products/api/v1.0/products/update_product", json=request_payload, headers = header)
    result = response.get_json()

    assert response.status_code == 400

    # Product not in DB
    request_payload = {"id": 100, "name":"update test"}
    response = client.put("/products/api/v1.0/products/update_product", json=request_payload,  headers = header)
    result = response.get_json()

    assert response.status_code == 404

    # Update correct entry
    request_payload = {"id": 1, "description": "updated test description"}
    response = client.put("/products/api/v1.0/products/update_product", json=request_payload,  headers = header)
    result = response.get_json()

    assert response.status_code == 200
    
def test_get_all_products(client):
    # Add correct product
    request_payload = {"name": "test product2", "description": "test description"}
    response = client.post("/products/api/v1.0/products/add_product", json=request_payload,  headers = header)

    # Test get all products
    response = client.get('/products/api/v1.0/products/get_all_products',  headers = header)

    assert response.status_code == 200

def test_get_one_product(client):
    # Add correct product
    request_payload = {"name": "test product2", "description": "test description"}
    response = client.post("/products/api/v1.0/products/add_product", json=request_payload,  headers = header)

    # No id in request
    request_payload = {"test" : "test"}
    response = client.get("/products/api/v1.0/products/get_product/", json=request_payload,  headers = header)

    assert response.status_code == 400

    # Correct product request
    request_payload = {"id" : 1}
    response = client.get("/products/api/v1.0/products/get_product/", json=request_payload,  headers = header)

    assert response.status_code == 200

def test_get_all_offers(client):
    # Add correct product
    request_payload = {"name": "test product2", "description": "test description"}
    response = client.post("/products/api/v1.0/products/add_product", json=request_payload,  headers = header)

    # Test get all offers
    response = client.get("/products/api/v1.0/products/get_all_offers", headers = header)

    assert response.status_code == 200

def test_get_offers_one_product(client):
    # Add correct product
    request_payload = {"name": "test product2", "description": "test description"}
    response = client.post("/products/api/v1.0/products/add_product", json=request_payload,  headers = header)

    # No id in request
    request_payload = {"test": "test"}
    response = client.get("/products/api/v1.0/products/get_offers_one_product/", json=request_payload,  headers = header)

    assert response.status_code == 400

    # Test get product
    request_payload = {"id": 1}
    response = client.get("/products/api/v1.0/products/get_offers_one_product/", json=request_payload,  headers = header)

    assert response.status_code == 200

def test_delete_product(client):
    # Add correct product
    request_payload = {"name": "test product2", "description": "test description"}
    response = client.post("/products/api/v1.0/products/add_product", json=request_payload,  headers = header)

    # No id in request
    request_payload = {"test": "test"}
    response= client.delete("/products/api/v1.0/products/delete_product/", json=request_payload,  headers = header)

    assert response.status_code == 400

    # No product in DB
    request_payload = {"id": 100}
    response= client.delete("/products/api/v1.0/products/delete_product/", json=request_payload,  headers = header)

    assert response.status_code == 404

    # Test delete product
    request_payload = {"id": 1}
    response= client.delete("/products/api/v1.0/products/delete_product/", json=request_payload,  headers = header)
    
    assert response.status_code == 200


