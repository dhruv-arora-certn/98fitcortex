from rest_framework import serializers , exceptions
from epilogue.models import Customer , LoginCustomer ,GeneratedDietPlan , GeneratedDietPlanFoodDetails , Food , Objective , CustomerFoodExclusions , CustomerMedicalConditions
from django.core.exceptions import ObjectDoesNotExist
from passlib.hash import bcrypt


class ObjectiveSerializer(serializers.ModelSerializer):
	class Meta:
		model = Objective
		fields = ["id" , "name"]

class CustomerSerializer(serializers.ModelSerializer):
	height = serializers.CharField(source = "h")
	weight = serializers.CharField(source = "w")
	gender = serializers.CharField(source = "gen")
	lifestyle = serializers.CharField(source = "ls")
	height_type = serializers.IntegerField(source = "h_type")
	weight_type = serializers.IntegerField(source = "w_type")

	class Meta:
		model = Customer
		fields = ["email" , "first_name" , "last_name" , "mobile" , "age" , "weight" , "height", "lifestyle" , "objective" , "id", "gender" , "body_type" , "food_cat" ,"weight_type" , "height_type"]


class FoodSerializer(serializers.ModelSerializer):
	class Meta:
		model = Food
		fields = ["name" , "protein" , "fat" , "carbohydrates" , "image"]

class DietPlanSerializer(serializers.ModelSerializer):
	protein = serializers.SerializerMethodField()
	fat = serializers.SerializerMethodField()
	carbohydrates = serializers.SerializerMethodField()
	image = serializers.CharField(source = "food_item.image")
	quantity = serializers.SerializerMethodField()
	weight = serializers.SerializerMethodField()
	dietplan_id = serializers.SerializerMethodField()
	unit = serializers.SerializerMethodField()

	class Meta:
		model = GeneratedDietPlanFoodDetails
		fields = "__all__"

	def get_factored_attr(self , attr , obj):
		factor = float(obj.calorie)/float(obj.food_item.calarie)
		return round(getattr(obj.food_item , attr) *factor , 2)

	def get_protein(self , obj):
		return self.get_factored_attr("protein", obj)

	def get_fat(self , obj):
		return self.get_factored_attr("fat", obj)

	def get_carbohydrates(self , obj):
		return self.get_factored_attr("carbohydrates", obj)

	def get_quantity(self , obj):
		if obj.quantity == 0:
			return obj.food_item.quantity
		return obj.quantity

	def get_weight(self , obj):
		if obj.weight == 0:
			return obj.food_item.weight
		return obj.weight

	def get_dietplan_id(self , obj):
		return obj.dietplan.id

	def get_unit(self,  obj):
		if obj.food_item.drink == 1:
			return 'ml'
		return 'gms'

class LoginSerializer(serializers.Serializer):
	email = serializers.EmailField(required = True)
	password = serializers.CharField(style ={'input_type' : 'password'})

	def validate(self , attrs):
		email = attrs.get('email')
		password = attrs.get('password')

		login_user = None
		login_user = LoginCustomer.objects.filter(email = email)	
		if login_user.count():
			print("login count")
			if self.authenticate(login_user.first() , password):
				attrs['user'] = Customer.objects.filter(email = email).first()
				return attrs
			raise exceptions.ValidationError("Unable to Login with credentials")
		raise exceptions.ValidationError("Unable to login with credentials")

	def authenticate(self , user , password):
		print("inside authenticate")
		return bcrypt.verify(password , user.password)

class CustomerFoodExclusionSerializer(serializers.ModelSerializer):

	
	class Meta:
		model = CustomerFoodExclusions
		fields = "__all__"

class CustomerMedicalConditionsSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = CustomerMedicalConditions
		fields = "__all__"

class CustomerObjectiveSerializer(serializers.ModelSerializer):
	class Meta:
		model = Objective
		fields = "__all__"
		
class CreateCustomerSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Customer
		fields = [ "email" , "first_name" , "last_name" , "mobile" , "age" , "weight" , "height", "lifestyle" , "objective" , "id", "gender" , "body_type" , "food_cat" , "auth_token",  "weight_type" , "height_type"]


	weight = serializers.CharField(source = "w")		
	height = serializers.CharField(source = "h")		
	auth_token = serializers.SerializerMethodField()
	gender = serializers.CharField(source = "gen")
	lifestyle = serializers.CharField(source = "ls")
	weight_type = serializers.IntegerField(source = "w_type")
	height_type = serializers.IntegerField(source = "h_type")

	def get_auth_token(self , obj):
		return obj.auth_token.key