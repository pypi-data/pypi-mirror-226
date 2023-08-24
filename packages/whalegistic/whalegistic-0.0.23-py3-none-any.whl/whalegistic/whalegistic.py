import jwt
import requests

class Whalegistic:

	def __init__(this, public_key, private_key):
		this.pri_key = private_key;
		this.pub_key = public_key;
		this.token = jwt.encode({ "public_key": public_key }, private_key, algorithm="HS256");
		print(f"TOKEN : {this.token}")



	def getBrands(this, send_obj):

		send_url = "https://whalegistic.com/api/get-brands"

		if send_obj == None: 
			send_obj = {}

		send_obj["public_key"] = this.pub_key

		send_headers = { 
			"Content-Type": "application/json", 
			"Authorization": f"Bearer {this.token}" 
		}

		response = requests.post(url = send_url, json = send_obj, headers = send_headers)
		brands_obj = response.json()

		return brands_obj["brands"];



	def getProducts(this, send_obj):

		send_url = "https://whalegistic.com/api/get-products"

		if send_obj == None: 
			send_obj = {}

		send_obj["public_key"] = this.pub_key

		send_headers = { 
			"Content-Type": "application/json", 
			"Authorization": f"Bearer {this.token}" 
		}

		response = requests.post(url = send_url, json = send_obj, headers = send_headers)
		products_obj = response.json()

		return products_obj["products"];
