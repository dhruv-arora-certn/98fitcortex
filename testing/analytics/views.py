from django.shortcuts import render

# Create your views here.
from analytics.serializers import CustomerTrackingSerializer ,  CustomerGoogleClientSerializer
from analytics.models import CustomerTracking , CustomerGoogleClient
from rest_framework import generics
from epilogue.authentication import CustomerAuthentication
from rest_framework import permissions

class CustomerGoogleClientView(generics.GenericAPIView):
	authentication_classes = [CustomerAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = CustomerGoogleClientSerializer

	def post(self, request , *args , **kwargs):
		user = request.user
		user.gaclienids.get_or_create()


