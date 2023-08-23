from PyJWT import jwt

class Whalegistic:

	def __init__(this, public_key, private_key):
		this.pri_key = private_key;
		this.pub_key = public_key;
		this.token = jwt.encode({ public_key: public_key}, private_key);

	def getBrands(this):
		print(f'JWT TOKEN : {this.token}')
