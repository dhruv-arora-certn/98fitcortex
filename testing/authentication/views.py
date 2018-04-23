from django.shortcuts import render
from django.core import signing

from authentication.serializers import RegistrationSerializer , GoogleLoginSerializer , FacebookLoginSerializer, BatraGoogleSerializer, DeviceRegistrationSerializer, ChangePasswordSerializer, ForgotPasswordOTPSerializer
from authentication import utils
from authentication import signals 

from rest_framework import generics
from rest_framework import response
from rest_framework import permissions
from rest_framework import status

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
			"key" : lc.customer.auth_token.key ,
			"id" : lc.customer.id
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
		return response.Response({
			"key" : request.user.auth_token.key,
			"id" : request.user.id 
		})

class GoogleLoginView(generics.GenericAPIView):
	serializer_class = GoogleLoginSerializer
	
	def post(self, request , *args, **kwargs):
		s = self.serializer_class(data = request.data , context = {
			'request' : request
		})
		s.is_valid(raise_exception = True)
		lc = s.save()
		return response.Response({
			"key" : lc.customer.auth_token.key ,
			"id" : lc.customer.id
		})

class FacebookLoginView(generics.GenericAPIView):
	serializer_class = FacebookLoginSerializer
	
	def post(self , request , *args , **kwargs):
		s = self.serializer_class(data = request.data , context = {
			'request' : request
		})
		s.is_valid(raise_exception = True)
		lc = s.save()
		return response.Response({
			"key" : lc.customer.auth_token.key ,
			"id" : lc.customer.id
		})

class BatraGoogleLoginView(generics.GenericAPIView):
	serializer_class = BatraGoogleSerializer

	def post(self , request , *args , **kwargs):
		s = self.serializer_class(
			data = request.data , context = {
				'request' : request
			}
		)
		s.is_valid(raise_exception = True)
		lc = s.save()
		return response.Response({
			"key" : lc.customer.auth_token.key ,
			"id" : lc.customer.id
		})

class DeviceRegistrationView(generics.CreateAPIView):
    serializer_class = DeviceRegistrationSerializer

    def create(self,request, *args, **kwargs):
        request.data.update({
            "customer" : request.user.pk
        })
        return super().create(request, *args, **kwargs)


class EmailVerificationView(generics.GenericAPIView):
    authentication_classes = [CustomerAuthentication]

    def post(self, request, *args, **kwargs):
        token = request.data.get("token")
        
        #Check if the token is invalid or expired
        try:
            email = utils.unsign(token, max_age = 86400 )
        except signing.BadSignature as bad_signature:
            return response.Response({
                "message" : "Invalid Token"
            }, status = status.HTTP_403_FORBIDDEN)
        except signing.SignatureExpired as expired_signature:
            return response.Response({
                "message" : "Token Expired"
            }, status = status.HTTP_403_FORBIDDEN)
        else:
            if email == request.user.email:
                #Add code for marking the user verified
                request.user.logincustomer.email_confirm = 'yes'
                request.user.logincustomer.save()
                return response.Response({
                    "message": "Successfully Verified"
                })
            return response.Response({
                "message" : "Account mismatch"
            }, status = status.HTTP_403_FORBIDDEN)

class EmailVerificationResendView(generics.GenericAPIView):
    authentication_classes = [CustomerAuthentication]

    def post(self, request, *args, **kwargs):
        if request.user.logincustomer.email_confirm == 'yes':
            return response.Response({
                "message" : "Already Verified"
            })
        else:
            signals.send_verification_email(sender = self, logincustomer = request.user.logincustomer)
            return response.Response({
                "message" : "Verification link sent"
            })

class OTPSendView(generics.GenericAPIView):
    authentication_classes = [CustomerAuthentication]
    serializer_class = ForgotPasswordOTPSerializer

    def post(self, request, *args, **kwargs):
        s = ForgotPasswordOTPSerializer(data = request.data, context = {
            'request' : request
        })
        s.is_valid(raise_exception = True)
        signature = s.save()
        return response.Response({
            "token" : signature
        })

class ChangePasswordView(generics.GenericAPIView):
    authentication_classes = [CustomerAuthentication]
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        s = self.serializer_class(data = request.data, context = {
            'request' : request
        }) 
        try:
            s.is_valid(raise_exception = True)
        except signing.SignatureExpired as e:
            return response.Response({
                "message": "OTP Expired"
            }, status = status.HTTP_403_FORBIDDEN)
        except signing.BadSignature as e:
            return response.Response({
                "message" : "Incorrect OTP"
            }, status = status.HTTP_403_FORBIDDEN)
        else:
            s.save()
            return response.Response({
                "message" : "Successfully Changed"
            })
