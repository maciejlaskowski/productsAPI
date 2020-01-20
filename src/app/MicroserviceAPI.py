# Products Microservice

from flask import Flask, request, make_response, jsonify, abort
import json
from apscheduler.schedulers.background import BackgroundScheduler

from AsqlDB import MicroserviceDB
from AofferMicroserviceConnection import OffersMicroservice


app = Flask(__name__)

db = MicroserviceDB()
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
    if not request.json or not "address" in request.json:
        abort(400)
    get = {
        "address" : request.json["address"]
    }
    offers.changeURL(get["address"])
    return ''

# Get all products
@app.route('/products/api/v1.0/products/get_all_products', methods=['GET'])
def get_products():
    if db.getProducts() == []:
        abort(404)
    return jsonify(db.getProducts())
    
# Get one product
@app.route('/products/api/v1.0/products/get_product/', methods=['GET'])
def get_product():
    if not request.json or not "id" in request.json:
        abort(400)
    if db.getProduct(request.json["id"]) == []:
        abort(404) 
    
    get = {
        "id" : request.json["id"]
    }

    return jsonify(db.getProduct(get["id"]))

# Get all offers
@app.route('/products/api/v1.0/products/get_all_offers', methods=['GET'])
def get_all_offers():
    if db.getOffers() == []:
        abort(404)

    return jsonify(db.getOffers())
    
# Get offers for one product
@app.route('/products/api/v1.0/products/get_offers_one_product/', methods=['GET'])
def get_offers_one_product():
    if not request.json or not "id" in request.json:
        abort(400)
    get = {
        "id" : request.json["id"]
    }
    if db.getOffer(get["id"]) == []:
        abort(404)

    return jsonify(db.getOffer(get["id"]))

# Add product
@app.route('/products/api/v1.0/products/add_product', methods=['POST'])
def add_product():
    if not request.json or not "name" in request.json or request.json["name"] == '':
        abort(400)
    if not isinstance(request.json["name"], str):
        abort(400)
    if "description" in request.json and not isinstance(request.json["description"], str):
        abort(400)
    
    product = {
        "name": request.json["name"],
        "description": request.json.get("description", "")
    }
    id = db.insertProduct(product["name"], product["description"])
    product["id"] = id
    offers.registerProduct(product)
    update_offers()

    return "Product added"

# Update product
@app.route('/products/api/v1.0/products/update_product', methods=['PUT'])
def update_prod():
    if not request.json or not "id" in request.json or request.json["id"] == '':
        abort(400)
    if "name" in request.json and not isinstance(request.json["name"], str):
        abort(400)
    if "description" in request.json and not isinstance(request.json["description"], str):
        abort(400)          
    if db.getProduct(request.json["id"]) == []:
        abort(404)

    update = {
        "id" : request.json["id"],
        "name": request.json.get("name", ""),
        "description": request.json.get("description", "")
    }

    db.updateProduct(id = int(update["id"]), name = update["name"], description = update["description"])
    offers.registerProduct({"id": int(update["id"]), "name":update["name"], "description":update["description"]})
    return 'Product updated'

# Delete product
@app.route('/products/api/v1.0/products/delete_product/', methods = ['DELETE'])
def delete_prod():
    if not request.json or not "id" in request.json or request.json["id"] == '':
       abort(400)
    elif db.getProduct(request.json["id"]) == []:
        abort(404)

    delete = {
        "id" : request.json["id"]
    }

    db.deleteProduct(str(delete["id"]))
    
    return ("Product deleted")

# Update Offers
def update_offers():
    products = db.getProducts()
    offersDB = json.dumps(db.getOffers())
    for product in products:
        offersResponse = offers.getOffers(str(product["id"]))
        for offer in offersResponse:
            if str(offer["id"]) not in offersDB:
                db.insertOffer(offer["id"], offer["price"], offer["items_in_stock"], product["id"])
            elif str(offer["id"]) in offersDB:
                db.updateOffer(offer["id"], offer["price"], offer["items_in_stock"])
    
    print("Offers updated")

# Background job scheduler
scheduler = BackgroundScheduler()
job = scheduler.add_job(update_offers, 'interval', minutes=1)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)