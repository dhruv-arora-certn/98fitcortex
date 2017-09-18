from django.shortcuts import render
from rest_framework import generics , response
from .serializers import SMSSerializer
# Create your views here.

class SendSMSView(generics.GenericAPIView):
	serializer_class = SMSSerializer 
	throttle_scope = "navratri-sms"

	def post(self, request , *args , **kwargs):
		s = self.serializer_class(data = request.data)
		s.is_valid(raise_exception = True)
		r = s.save()
		return response.Response({
			'message' : "Success"
		})
