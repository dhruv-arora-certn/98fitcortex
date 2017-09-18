from  .settings import *
import requests

class SMS():

	baseURL = "https://control.msg91.com/api/sendhttp.php"

	def __init__(self , number=None ,message = None):
		self.number = number
		self.message = message
	
	def send(self):
		url =  self.baseURL
		r = requests.get(url , params = {
			'authkey' : MSG91_KEY,
			'mobiles' : self.number,
			'sender' : 'FITNES',
			'route' : 4,
			'message' : self.message
		})
		r.raise_for_status()
		return r
