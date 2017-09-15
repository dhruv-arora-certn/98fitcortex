from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import _extract_id_token 
import requests
import httplib2
import os

class GoogleAdapter:

	def __init__(self , auth_code = None , access_token =  None):
		self.auth_code = auth_code
		self.access_token = access_token

	def complete_login(self):
		self.credentials = _extract_id_token(self.access_token)
		return self.credentials	

class FacebookAdapter:

	def __init__(self , access_token ) :
		self.access_token = access_token


	def complete_login(self):
		params = {
			"fields" : "first_name,email,last_name,picture",
			"access_token" : self.access_token
		}
		r = requests.get("https://graph.facebook.com/v2.5/me" , params = params)
		self.response = r
		r.raise_for_status()
		return r.json()
