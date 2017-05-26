from rest_framework import serializers , exceptions
from epilogue.models import Customer , LoginCustomer ,GeneratedDietPlan , GeneratedDietPlanFoodDetails , Food , Objective
from django.core.exceptions import ObjectDoesNotExist
from passlib.hash import bcrypt


class ObjectiveSerializer(serializers.ModelSerializer):
	class Meta:
		model = Objective
		fields = ["id" , "name"]

class CustomerSerializer(serializers.ModelSerializer):
	height = serializers.FloatField(source = "h")
	weight = serializers.FloatField(source = "w")
	objective = ObjectiveSerializer()
	gender = serializers.CharField(source = "gen")
	lifestyle = serializers.CharField(source = "ls")
		
	class Meta:
		model = Customer
		fields = ["email" , "first_name" , "last_name" , "mobile" , "age" , "weight" , "height", "lifestyle" , "objective" , "id", "gender"]

	def update(self , instance , validated_data):
		objective = validated_data.pop('objective' , {})
		# import ipdb
		# ipdb.set_trace()
		a = super().update(instance , validated_data )
		if objective : 
			o = Objective.objects.get(name = objective['name'])
			a.objective = o
			a.save()
		return a 



class FoodSerializer(serializers.ModelSerializer):
	class Meta:
		model = Food
		fields = ["name" , "protein" , "fat" , "carbohydrates"]

class DietPlanSerializer(serializers.ModelSerializer):
	# food_item = FoodSerializer(read_only = True)
	protein = serializers.SerializerMethodField()
	fat = serializers.SerializerMethodField()
	carbohydrates = serializers.SerializerMethodField()

	class Meta:
		model = GeneratedDietPlanFoodDetails
		fields = "__all__"

	def get_factored_attr(self , attr , obj):
		factor = float(obj.calorie)/float(obj.food_item.calarie)
		return getattr(obj.food_item , attr) *factor

	def get_protein(self , obj):
		return self.get_factored_attr("protein", obj)

	def get_fat(self , obj):
		return self.get_factored_attr("fat", obj)

	def get_carbohydrates(self , obj):
		return self.get_factored_attr("carbohydrates", obj)


class LoginSerializer(serializers.Serializer):
	email = serializers.EmailField(required = True)
	password = serializers.CharField(style ={'input_type' : 'password'})

	def validate(self , attrs):
		print("Calling Validate")
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