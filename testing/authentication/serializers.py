from rest_framework import serializers , exceptions
from epilogue.serializers import LoginSerializer
from epilogue.models import LoginCustomer , Customer
from django.contrib.auth import password_validation
from authentication.exceptions import UserAlreadyExists
from passlib.hash import bcrypt
from analytics.models import UserSignupSource
from .adapters import GoogleAdapter  , FacebookAdapter
from .signals import navratri_signup
import ipdb 

class BaseRegistrationSerializer(serializers.Serializer):
	
	def user_create(self , validated_data):
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
			customer.email = validated_data['email']
			customer.save()
			return lc
		else:
			email = validated_data['email']
			c = Customer.objects.create(
				email = email
			)
			lc = LoginCustomer.objects.create(
				email = email,
				password = bcrypt.hash(validated_data['password']),
				customer = c
			)
			return lc


class BaseSocialSerializer(serializers.Serializer):

	def create(self , credentials):

		email , first_name , last_name , picture = self.release_attrs(credentials)

		try:
			l = LoginCustomer.objects.get(email = email)
		except LoginCustomer.DoesNotExist as e:
			if self.context['request'].user.is_anonymous:
				print(email)
				customer,created = Customer.objects.get_or_create(email = email)
				customer.image = picture
				customer.save()
				lc = LoginCustomer.objects.create(
					email = email,
					first_name = customer.first_name or first_name,
					customer = customer
				)
				return lc
			else:
				customer = self.context.get("request").user
				if customer.email  and customer.email != email:
					raise exceptions.ValidationError("Conflicting Email Addresses")
				customer.image = picture
				customer.email = email
				customer.save()
				lc , created = LoginCustomer.objects.get_or_create(
					email = email,
					first_name = customer.first_name or first_name,
					customer = customer
				)
				return lc
		return l


class RegistrationSerializer(BaseRegistrationSerializer):
	email = serializers.EmailField()
	password = serializers.CharField()

	def create(self , validated_data):
		return super().user_create(validated_data)

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

class GoogleLoginSerializer(BaseSocialSerializer):
	access_token = serializers.CharField() 

	def release_attrs(self , credentials):
		return credentials['email'] , credentials['name'] ,"" , credentials['picture']

	def validate(self ,attrs):
		adapter = GoogleAdapter(
			access_token = attrs.get('access_token')
		)
		try:
			credentials = adapter.complete_login()
			if not self.context['request'].user.is_anonymous and self.context['request'].user.email  :
				assert credentials['email'] == self.context['request'].user.email , exceptions.ValidationError("Conflicting Email Addresses")
		except Exception as e:
			raise exceptions.ValidationError(e)
		else:
			return credentials


class FacebookLoginSerializer(BaseSocialSerializer):
	access_token = serializers.CharField()

	def release_attrs(self , credentials):
		return credentials['email'] , credentials['first_name'] , credentials['last_name'] , credentials['picture']['data']['url']

	def validate(self , attrs):
		adapter = FacebookAdapter(
			access_token = attrs['access_token']
		)
		try:
			credentials = adapter.complete_login()
		except Exception as e:
			#Facebook returns an error
			raise exceptions.ValidationError(e)
		else:
			#Facebook Returns the credentials
			if not self.context['request'].user.is_anonymous and self.context['request'].user.email  :
				if not credentials['email'] == self.context['request'].user.email:
					raise exceptions.ValidationError("Conflicting Email Addresses")
			return credentials

class BatraGoogleSerializer(BaseSocialSerializer):
	email = serializers.EmailField()
	name = serializers.CharField()
	picture = serializers.CharField()
	url = serializers.URLField()
	source = serializers.CharField(required = False)
	language = serializers.CharField()

	def validate_language(self , lang):
		if lang not in ("en" , "hi"):
			raise exceptions.ValidationError("Not a valid language")
		return lang

	def release_attrs(self, credentials):
		return credentials['email'], credentials['name'] , '' , credentials['picture']

	def create(self,validated_data):
		created = super().create(validated_data)
		email = validated_data['email']
		url = validated_data['url']
		language = validated_data['language']

		created.customer.first_name = validated_data['name']
		created.customer.save()
		signupsource = UserSignupSource.objects.create(
			customer = created.customer,
			source = validated_data['source'],
			campaign = "navratri",
			language = language
		)
		navratri_signup.send(sender = LoginCustomer , email = email , url = url , lang = language)
		return created
