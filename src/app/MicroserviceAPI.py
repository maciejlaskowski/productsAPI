# Products Microservice

from flask import Flask, request, make_response, jsonify, abort
import json
from apscheduler.schedulers.background import BackgroundScheduler

from AsqlDB import MicroserviceDB
from AofferMicroserviceConnection import OffersMicroservice


app = Flask(__name__)

# Create DB instance
db = MicroserviceDB()
# Create Offers microservice connection instance
offers = OffersMicroservice()

# Error messages
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def wrong_request(error):
    return make_response(jsonify({'error': 'Wrong request'}), 400)

# Change Offers MS URL
@app.route('/api/v1.0/configure_offers', methods=['PUT'])
def configure_offers():
    # Handle errors
    if not request.json or not "address" in request.json:
        abort(400)
    # Get request content
    get = {
        "address" : request.json["address"]
    }
    # Call offers instance to change URL
    offers.changeURL(get["address"])
    return ''

# Get all products
@app.route('/products/api/v1.0/products/get_all_products', methods=['GET'])
def get_products():
    # Handle errors
    if db.getProducts() == []:
        abort(404)
    return jsonify(db.getProducts())
    
# Get one product
@app.route('/products/api/v1.0/products/get_product/', methods=['GET'])
def get_product():
    # Handle errors
    if not request.json or not "id" in request.json:
        abort(400)
    if db.getProduct(request.json["id"]) == []:
        abort(404) 
    # Get request content
    get = {
        "id" : request.json["id"]
    }

    return jsonify(db.getProduct(get["id"]))

# Get all offers
@app.route('/products/api/v1.0/products/get_all_offers', methods=['GET'])
def get_all_offers():
    # Handle errors
    if db.getOffers() == []:
        abort(404)

    return jsonify(db.getOffers())
    
# Get offers for one product
@app.route('/products/api/v1.0/products/get_offers_one_product/', methods=['GET'])
def get_offers_one_product():
    # Handle errors
    if not request.json or not "id" in request.json:
        abort(400)
    # Get request content 
    get = {
        "id" : request.json["id"]
    }
    # Handle errors
    if db.getOffer(get["id"]) == []:
        abort(404)

    return jsonify(db.getOffer(get["id"]))

# Add product
@app.route('/products/api/v1.0/products/add_product', methods=['POST'])
def add_product():
    # Handle errors
    if not request.json or not "name" in request.json or request.json["name"] == '':
        abort(400)
    if not isinstance(request.json["name"], str):
        abort(400)
    if "description" in request.json and not isinstance(request.json["description"], str):
        abort(400)
    # Get request content
    product = {
        "name": request.json["name"],
        "description": request.json.get("description", "")
    }
    # registed new product in the DB and get ID
    id = db.insertProduct(product["name"], product["description"])
    # Add ID to product data
    product["id"] = id
    # Registe new product in Offers microservice
    offers.registerProduct(product)
    # Update offers for products
    update_offers()

    return "Product added"

# Update product
@app.route('/products/api/v1.0/products/update_product', methods=['PUT'])
def update_prod():
    # Handle errors
    if not request.json or not "id" in request.json or request.json["id"] == '':
        abort(400)
    if "name" in request.json and not isinstance(request.json["name"], str):
        abort(400)
    if "description" in request.json and not isinstance(request.json["description"], str):
        abort(400)          
    if db.getProduct(request.json["id"]) == []:
        abort(404)
    # Get request content
    update = {
        "id" : request.json["id"],
        "name": request.json.get("name", ""),
        "description": request.json.get("description", "")
    }
    # Update product in the DB
    db.updateProduct(id = int(update["id"]), name = update["name"], description = update["description"])
    # Re-register product in the Offers service
    offers.registerProduct({"id": int(update["id"]), "name":update["name"], "description":update["description"]})
    return 'Product updated'

# Delete product
@app.route('/products/api/v1.0/products/delete_product/', methods = ['DELETE'])
def delete_prod():
    # Handle errors
    if not request.json or not "id" in request.json or request.json["id"] == '':
       abort(400)
    elif db.getProduct(request.json["id"]) == []:
        abort(404)
    # Get request content
    delete = {
        "id" : request.json["id"]
    }
    # Call DB to delete product
    db.deleteProduct(str(delete["id"]))
    
    return ("Product deleted")

# Update Offers
def update_offers():
    # Get products list from DB
    products = db.getProducts()
    # Get offers list from DB
    offersDB = json.dumps(db.getOffers())
    # Loop through products
    for product in products:
        # Get offers for product from Offers microservice
        offersResponse = offers.getOffers(str(product["id"]))
        # Loop through offers in the response
        for offer in offersResponse:
            # If an offer is not in the DB insert it
            if str(offer["id"]) not in offersDB:
                db.insertOffer(offer["id"], offer["price"], offer["items_in_stock"], product["id"])
            # If an offer is in the DB update it
            elif str(offer["id"]) in offersDB:
                db.updateOffer(offer["id"], offer["price"], offer["items_in_stock"])
    
    print("Offers updated")

# Background job scheduler
scheduler = BackgroundScheduler()
job = scheduler.add_job(update_offers, 'interval', minutes=1)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=False)