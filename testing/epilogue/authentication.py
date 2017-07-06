from rest_framework.authentication import TokenAuthentication
from epilogue.models import Token

class CustomerAuthentication(TokenAuthentication):
	model = Token

	def __init__(self , *args , **kwargs):
		print(args)
		print(kwargs)
		print("Calling Customer Authentication ")
		super().__init__(*args , **kwargs)