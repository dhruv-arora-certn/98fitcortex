from django.shortcuts import render

# Create your views here.
from . import serializers, models

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions

from epilogue.authentication import CustomerAuthentication


class CustomerGoogleClientView(generics.GenericAPIView):
	authentication_classes = [CustomerAuthentication]
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = serializers.CustomerGoogleClientSerializer

	def post(self, request , *args , **kwargs):
		data = {
			'customer' : request.user.id,
			'clientId' : request.data.get('clientId')
		}
		serializer = self.serializer_class(data = data)
		serializer.is_valid(raise_exception = True)
		serializer.save()
		return Response(serializer.data)


class CustomerTrackingView(generics.CreateAPIView):
	serializer_class = serializers.CustomerTrackingSerializer

class EventPageTrackingView(generics.CreateAPIView):
	serializer_class = serializers.EventPageTrackingSerializer

class EventMailingView(generics.CreateAPIView):
    pass

class UserFeedbackView(generics.CreateAPIView):
    serializer_class = serializers.UserFeedbackSerializer
