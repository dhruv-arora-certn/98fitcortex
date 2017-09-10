from rest_framework import serializers
from epilogue.serializers import LoginSerializer
from epilogue.models import LoginCustomer , Customer
from django.contrib.auth import password_validation
from authentication.exceptions import UserAlreadyExists
from passlib.hash import bcrypt
import ipdb 

class RegistrationSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()

	def create(self , validated_data):
		'''
		Create an instance of LoginCustomer.
		If the ERPCustomer is present in the request, bind the LoginCustomer instance to it. Otherwise create ERPCustomer Instance as well.
		'''
		if not getattr(self.context.get("request") , "user").is_anonymous:
			#ERPCustomer Exists
			customer = self.context.get("request").user
			if hasattr(customer , "logincustomer"):
				raise UserAlreadyExists("Account With this email already exists")
			lc = LoginCustomer.objects.create(
				email = validated_data['email'],
				password = bcrypt.hash(validated_data["password"]),
				customer = self.context['request'].user
			)
			return lc
		else:
			c = Customer.objects.create(
				email = validated_data['email']
			)
			lc = LoginCustomer.objects.create(
				email = validated_data['email'],
				password = bcrypt.hash(validated_data['password']),
				customer = c
			)
			return lc

	def validate_email(self , email ):
		print("Calling Validate Email")
		l = LoginCustomer.objects.filter(email = email)
		if l:
			raise UserAlreadyExists("This Email is already Registered")
		return email
	
	def validate_password(self , password):
		validators = [
			password_validation.NumericPasswordValidator,
			password_validation.MinimumLengthValidator({"min_length" : 7}),
			password_validation.CommonPasswordValidator
		]
		password_validation.validate_password(password , validators)
		return password

class GoogleLoginSerializer(serializers.Serializer):
	pass

class FacebookLoginSerializer(serializers.Serializer):
	pass

