import requests
import json


class OffersMicroservice:
    def __init__(self): 
    # Offers microservice address
        self.__offersAddress = "https://applifting-python-excercise-ms.herokuapp.com/api/v1/"
    # Get Token and set up header
        self.__head = self.__getAccessTokenHeader()
    
    # Change offers URL
    def changeURL(self, url):
        self.__offersAddress = str(url)
        
    # Get access Token
    def __getAccessTokenHeader(self):
        reqToken = requests.post(self.__offersAddress + 'auth/')
        authRequest = json.loads(reqToken.text)
        accessToken = authRequest.get('access_token')
        return {"Bearer": accessToken}
        
    # Register the product in Offers microservice
    def registerProduct(self, product):
        regProduct = requests.post(self.__offersAddress + 'products/register/', headers = self.__head, data = product)
        
    # Get offers from Offers microservice
    def getOffers(self, product_id):
        product_id = str(product_id)
        getOffer = requests.get(self.__offersAddress + 'products/' + product_id + '/offers', headers = self.__head)

        return json.loads(getOffer.text)

