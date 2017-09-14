from oauth2client.client import OAuth2WebServerFlow
import httplib2
import os

class GoogleAdapter:
	
	def __init__(self , auth_code , access_token =  None):
		self.auth_code = auth_code
		self.access_token = access_token
		
		self.flow = OAuth2WebServerFlow(
			client_id = os.environ.get("google_client_id"),
			client_secret = os.environ.get("google_client_secret"),
			scope = ["profile", "email"],
			redirect_uri = "http://localhost:8000/oauth2callback"
		)

	def complete_login(self):
		self.credentials = self.flow.step2_exchange(self.auth_code)
		self.credentials.authorize(httplib2.Http())
		return self.credentials	

class FacebookAdapter:
	pass
