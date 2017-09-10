from django.shortcuts import render
from authentication.serializers import RegistrationSerializer
from rest_framework import generics
from rest_framework import response
from rest_framework import permissions
from epilogue.models import LoginCustomer , Customer
from epilogue.authentication import CustomerAuthentication
# Create your views here.



class RegistrationView(generics.GenericAPIView):
	serializer_class = RegistrationSerializer
	queryset = LoginCustomer

	def post(self, request , *args, **kwargs):
		s = self.serializer_class(data = request.data , context = {
			'request' : request
		})
		s.is_valid(raise_exception = True)
		lc = s.save()
		return response.Response({
			"key" : lc.customer.auth_token.key 
		})

class AccountAssociationView(generics.GenericAPIView):
	serializer_class = RegistrationSerializer
	queryset = LoginCustomer
	authentication_classes = [CustomerAuthentication] 
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request , *args, **kwargs):
		s = self.serializer_class(
			data = request.data,
			context = {
				'request' : request
			}
		)
		s.is_valid(raise_exception = True)
		lc = s.save()
		return Response({
			"key" : request.user.auth_token.key
		})
