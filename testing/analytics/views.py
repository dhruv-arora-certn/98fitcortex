from django.shortcuts import render

# Create your views here.
from analytics.serializers import CustomerTrackingSerializer ,  CustomerGoogleClientSerializer
from analytics.models import CustomerTracking , CustomerGoogleClient
from rest_framework import generics
from rest_framework.response import Response
from epilogue.authentication import CustomerAuthentication
from rest_framework import permissions

class CustomerGoogleClientView(generics.GenericAPIView):
	authentication_classes = [CustomerAuthentication]
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = CustomerGoogleClientSerializer

	def post(self, request , *args , **kwargs):
		data = {
			'customer' : request.user.id,
			'clientId' : request.data.get('clientId')
		}
		serializer = CustomerGoogleClientSerializer(data = data)
		serializer.is_valid(raise_exception = True)
		serializer.save()
		return Response(serializer.data)


class CustomerTrackingView(generics.CreateAPIView):
	serializer_class = CustomerTrackingSerializer

