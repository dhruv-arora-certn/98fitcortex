from django.db import models
from dietplan.goals import Goals
from dietplan.gender import Male , Female
from epilogue.managers import *
from django.db.models.expressions import RawSQL
from django.db.models import Max
from rest_framework import exceptions
#Model Managers for Food Model

QUANTITY_MANIPULATE = [
	"Parantha",
	"Roti",
	"Dosa",
	"Cheela",
	"Uttapam"
]
UNCHANGABLE_ITEMS = [
	'Boiled Egg White',
	'Salad'
]
fieldMapper = {
		Goals.WeightLoss : "squared_diff_weight_loss",
		Goals.MaintainWeight : "squared_diff_weight_maintain",
		Goals.WeightGain : "squared_diff_weight_gain",
		Goals.MuscleGain : "squared_diff_muscle_gain"
}

exclusionMapper = {
	'wheat' : models.Q(wheat = 0),
	'nuts' : models.Q(nuts = 0),
	'dairy' : models.Q(dairy = 0),
	'lamb_mutton' : models.Q(lamb_mutton = 0),
	'beef' : models.Q(dairy = 0),
	'seafood' : models.Q(seafood = 0),
	'poultary' : models.Q(poultary = 0),
	'meat' : models.Q(meat = 0),
	'egg' : models.Q(egg = 0)
}
	
class Food(models.Model):
	name = models.TextField()
	quantity = models.IntegerField()
	calarie = models.FloatField()
	serving = models.TextField()
	size = models.CharField(max_length = 100)
	weight = models.FloatField()
	fat = models.FloatField()
	protein = models.FloatField()
	carbohydrates = models.FloatField()
	m1 = models.IntegerField()
	m2 = models.IntegerField()
	m3 = models.IntegerField()
	m4 = models.IntegerField()

	m5_loss = models.IntegerField()
	m5_gain = models.IntegerField()
	m5_stable = models.IntegerField()
	
	fruit = models.IntegerField()
	drink = models.IntegerField()
	dairy = models.IntegerField()
	snaks = models.IntegerField()
	vegetable = models.IntegerField()
	cereal_grains = models.IntegerField()
	salad = models.IntegerField()
	yogurt = models.IntegerField()
	dessert = models.IntegerField()
	pulses = models.IntegerField()
	for_loss = models.IntegerField()
	wheat = models.IntegerField()
	lamb_mutton = models.IntegerField()
	beef = models.IntegerField()
	seafood = models.IntegerField()
	poultary = models.IntegerField()
	meat = models.IntegerField()
	egg = models.IntegerField()

	cuisine = models.TextField()
	nuts = models.IntegerField()
	calcium = models.FloatField()
	vitaminc = models.FloatField()
	iron = models.FloatField()
	image_name = models.CharField(max_length = 100)
	squared_diff_weight_loss = models.FloatField(default = 0)
	squared_diff_weight_maintain = models.FloatField(default = 0)
	squared_diff_weight_gain = models.FloatField(default = 0)
	image_name = models.CharField(max_length = 100)

	def __init__(self , *args , **kwargs):
		super().__init__(*args , **kwargs)
		self.squared_diff_muscle_gain = self.squared_diff_weight_gain

	factor = 1

	def pcf_value(self): 
		return sum(
			[ 
				self.protein/protein_ideal,
				self.carbohydrates/carb_ideal,
				self.fat/fat_ideal
			]
		)

	def amplify(self , factor):
		self.weight = self.weight*2
		self.calarie = self.calarie*2
		return self

	@property
	def calorie(self):
		return round(self.calarie)

	objects = Default()
	m1_objects = M1()
	m2_objects = M2()
	m3_objects = M3()
	m4_objects = M4()
	m5loss_objects = M5_Loss()
	m5gain_objects = M5_Gain()
	m5stable_objects = M5_Stable()
		

	@classmethod
	def set_context(self, context):
		self.context = context

	def __str__(self):
		return self.name

	def update(self,factor):
		self.protein *= factor
		self.fat *= factor
		self.carbohydrates *= factor
		self.calarie *= factor
		self.calcium *= factor
		
	def update_weight(self, factor):
		new_weight = self.weight * factor
		new_weight = int( 5 * round(new_weight/5))
		self.update(new_weight/self.weight)
		return self
			
	def update_quantity(self ,factor):
		self.quantity *= factor
		self.quantity = round(self.quantity 	)
		self.update(factor)
		return self

	def goal_nutrition(self,goal):
		return self.protein*goal.protein + self.fat*goal.fat + self.carbohydrates*goal.carbs

	@property
	def image(self):
		if not self.image_name:
			return "http://98fit.com//webroot/dietlist_images/images.jpg"
		return "https://s3-ap-southeast-1.amazonaws.com/98fitasset/image/diet/%s"%(self.image_name)

	@classmethod
	def find(self , *args):
		q = models.Q()
		for e in args:
			q &= models.Q(name__contains = e)
		return self.objects.filter(q)

	@property
	def unit(self):
		if self.drink == 1:
			return 'ml'
		return 'gms'

	class Meta:
		db_table = "business_diet_list"
		managed = False


class Objective(models.Model):
	class Meta:
		managed = False
		db_table = "glo_objective"
	name = models.CharField(max_length = 50)

	@property
	def goal(self):
		if self.name == "Weight Loss":
			return Goals.WeightLoss
		if self.name == "Weight Gain":
			return Goals.WeightGain
		if self.name == "Muscle Gain":
			return Goals.MuscleGain
		if self.name == "Be Healthy":
			return Goals.MaintainWeight	

class Customer(models.Model):
	class Meta:	
		db_table = "erp_customer"
		managed = False

	VEG = 'veg'
	NONVEG = 'nonveg'
	EGG = 'egg'
	food_cat_choices = (
		(VEG , 'veg'),
		(NONVEG , 'nonveg'),
		(EGG , 'egg')
	)		
	email = models.CharField(max_length = 255 , blank = True)
	first_name = models.CharField(max_length = 25, blank = True)
	last_name = models.CharField(max_length = 25 , blank = True , null = True)
	create_on = models.DateTimeField(auto_now_add = True)
	mobile = models.CharField(max_length = 11 , blank = True , null = True)
	age = models.IntegerField( blank = True)
	w = models.CharField(db_column = "weight", max_length = 11 , blank = True)
	w_type = models.IntegerField(db_column = "weight_type")
	h = models.CharField(db_column = "height", max_length = 20, blank = True )
	h_type = models.IntegerField(db_column = "height_type")
	ls = models.CharField( max_length = 50 , db_column = "lifestyle" , blank = True)
	objective = models.ForeignKey(Objective , db_column = "objective", blank = True)
	gen = models.CharField(max_length = 20 , db_column = "gender", blank = True)
	body_type = models.CharField(max_length = 50, blank = True)
	food_cat = models.CharField(max_length = 50 , choices=  food_cat_choices, blank = True)

	is_authenticated = True

	@property
	def plans(self):
		return {
			e.week_id : e.dayWisePlan for e in self.generateddietplan_set.all()
		}

	@property
	def height(self):
		'''
		Convert the persisted height to meters
		'''
		if self.h_type == 1: #Feets and inches
			val =  float(self.h)*0.3048
		if self.h_type == 2: #Centimeters
			val =  self.h/100
		return round(val , 2)

	@property
	def weight(self):
		if int(self.w_type) == 1:
			val = float(self.w)
		if int(self.w_type) == 2:
			val = float(self.w * 0.4536)
		return round(val , 2)

	@property
	def goal(self):
		return self.objective.goal

	@property
	def gender(self):
		if self.gen == "male":
			return Male
		if self.gen == "female":
			return Female

	@property
	def lifestyle(self):
		return float(self.ls) if self.ls else None

	@property
	def lifestyle_string(self):
		if self.lifestyle == 1.2:
			return "Sedentary"
		if self.lifestyle == 1.37:
			return "Lightly Active"
		if self.lifestyle == 1.55:
			return "Moderately Active"
		if self.lifestyle == 1.70:
			return "Very Active"
		if self.lifestyle == 1.9:
			return "Extra Active"
			
	@property
	def is_active(self):
		return True

	def get_exclusions(self):
		q = models.Q()
		for e in self.customerfoodexclusions_set.all():
			q &= exclusionMapper.get(e.food_type) 
		return q	

	@property
	def medical_conditions_string(self):
		return ', '.join(e.condition_name.title() for e in self.customermedicalconditions_set.all()) or "None"

	@property
	def food_exclusions_string(self):
		return ', '.join(e.get_food_type_display().title() for e in self.customerfoodexclusions_set.all()) or "None"

	@property
	def latest_weight(self):
		last_weight = CustomerWeightRecord.latest_record(customer = self)
		if last_weight:
			return last_weight.weight
		return self.weight

	@property
	def weight_type(self):
		if self.w_type == 1:
			return "Kgs"
		if self.w_type == 2:
			return "Lbs"

	@property
	def height_type(self):
		if self.h_type == 1:
			return "Ft"
		if self.h_type == 2:
			return "Cms"

	def __str__(self):
		return self.first_name + " : " + self.email

class BusinessCustomer(models.Model):
	class Meta:
		db_table = "business_account"
		managed = False

	business_name = models.CharField(max_length = 100)
	business_owner_first_name = models.CharField( max_length = 25)
	business_owner_last_name = models.CharField( max_length = 25)
	mobile_number = models.CharField(max_length = 11)
	created_on = models.DateTimeField()
	signup_completed = models.CharField( max_length = 10)
	
	@property
	def name(self):
		return self.business_owner_first_name



class GeneratedDietPlan(models.Model):
	'''
	Store a weekly generated dietplan here
	'''
	class Meta:
		db_table = "erp_diet_plan"
		managed = False

	customer = models.ForeignKey(Customer , db_column = "erp_customer_id")
	created_on = models.DateTimeField(auto_now_add = True)
	user_week_id = models.IntegerField(default = 1)
	week_id = models.IntegerField(default = 1)
	company_id = models.IntegerField(default = 0)
	plan_type = models.CharField(max_length = 50 , default = "system generated plan")
	medi_applicable = models.CharField(max_length = 20 , default = "")

	@property
	def dayWisePlan(self):
		return {
			e : GeneratedDietPlanFoodDetails.objects.filter(models.Q(dietplan = self) & models.Q(day = e)).all() for e in range(1,8)
		}

	def changeMeal(self , day = None , meal = None):
		assert day , meal
		assert meal in ["m1" , "m2" , "m3" , "m4" , "m5"]
		items = GeneratedDietPlanFoodDetails.objects.filter(dietplan__id = self.id).filter(day = day).filter(meal_type = meal)
		for e in items:
			if e.food_name not in UNCHANGABLE_ITEMS:
				e.find_closest(save = True)
		return items

	def get_last_days(self , days):
		assert days > 0 and days <= 7
		baseQ = GeneratedDietPlanFoodDetails.objects.filter(dietplan__id = self.id)
		max_day = baseQ.aggregate(Max('day')).get("day__max") or 7
		print("Max Day " , max_day)
		items = []
		for day in range(max_day , max_day - days , -1):
			items.extend(baseQ.filter(day = day).values_list('food_name' , flat = True ))
		return items

	def regenerate(self):
		
		#Avoiding circular import
		from dietplan.generator import Pipeline
		
		self.pipeline = Pipeline(
			self.customer.latest_weight,
			self.customer.height, 
			float(self.customer.lifestyle),
			self.customer.goal,
			self.customer.gender.number,
			user = self.customer,
			dietplan = self,
			persist = True
		)
		self.pipeline.regenerate()

	@property
	def items(self):
		return list(self.generateddietplanfooddetails_set.values_list("food_name" , flat = True))

class GeneratedDietPlanFoodDetails(models.Model):
	'''
	Store the generated diet plan of a day here
	'''
	class Meta:
		managed = False
		db_table = "erp_diet_plan_food_details"

	dietplan = models.ForeignKey(GeneratedDietPlan , db_column = "erp_diet_plan_id" ) 
	food_item = models.ForeignKey(Food , db_column = "business_diet_list_id")
	food_name = models.CharField(max_length = 255)
	meal_type = models.CharField(max_length = 20)
	day = models.IntegerField()
	calorie = models.CharField(max_length = 50)
	weight = models.FloatField(default = 0)
	quantity = models.FloatField(default = 0)
	size = models.CharField(max_length = 50)
	day1 = Day1()
	day2 = Day2()
	day3 = Day3()
	day4 = Day4()
	day5 = Day5()
	day6 = Day6()
	day7 = Day7()
	objects = models.Manager()

	@property
	def factor(self):
		return float(self.calorie)/self.food_item.calarie

	def find_closest(self, save = False):
		'''
		*args represent the additional arguments that might be required in futurej
		'''
		if self.food_name in UNCHANGABLE_ITEMS:
			return self

		goal = self.dietplan.customer.goal
		old_food = self.food_item
		field = fieldMapper.get(goal)
		item = self.food_item
		
		if self.meal_type.endswith(("1" , "2" , "3" , "4")):
			f = getattr(Food , self.meal_type + "_objects")
		elif self.meal_type.endswith("5"):
			if goal == Goals.WeightLoss:
				f = getattr(Food , "m5loss_objects")
			if goal == Goals.WeightGain or goal == Goals.MuscleGain:
				f = getattr(Food , "m5gain_objects")
			if goal == Goals.MaintainWeight:
				f = getattr(Food , "m5stable_objects")

		#Gather objects to exclude
		to_exclude = self.dietplan.items
		to_exclude.extend(self.old_suggestions)
		
		#Generating query 
		f = f.exclude(name__in = to_exclude)
		f = f.filter(fruit = item.fruit).filter(drink = item.drink).filter(dairy = item.dairy).filter(snaks = item.snaks).filter(vegetable = item.vegetable).filter(cereal_grains = item.cereal_grains).filter(salad = item.salad).filter(yogurt = item.yogurt).filter(dessert=  item.dessert).filter(pulses = item.pulses).filter(cuisine = item.cuisine).filter(nuts = item.nuts) or item

		f = f.annotate(d = RawSQL("Abs(%s - %s)" , [field , getattr(self.food_item,field)])).exclude(id = self.food_item_id).order_by("d").order_by(field)
		print("Old item" , self.food_item)
		print("New item" , f)
		if not f:
			raise exceptions.NotFound()

		self.food_item = f
		if any(x in f.name for x in QUANTITY_MANIPULATE ):
			f.update_quantity(self.factor)
		else:
			f.update_weight(self.factor)
		self.update_attrs(f)
		if save:
			print("Saving Changed Dish")
			new_suggestion = DishReplacementSuggestions.objects.create(food = old_food , dietplan_food_details = self)
			self.save()

		return self

	@property
	def old_suggestions(self):
		return list(self.dishreplacementsuggestions_set.values_list('food__name' , flat = True))

	def update_attrs(self , item):
		self.calorie = str(item.calarie)
		self.weight = item.weight
		self.quantity = item.quantity
		self.size = item.size
		self.food_name = item.name
		return self


class GeneratedExercisePlan(models.Model):
	class Meta:
		db_table = "erp_exercise_plan"
		managed = False
	
	customer = models.ForeignKey(Customer , db_column = "erp_customer_id")
	created_on = models.DateTimeField(default = None)

import binascii
import os

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Token(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.OneToOneField(
        Customer, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name=_("Customer")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/encode/django-rest-framework/issues/705
        abstract = 'rest_framework.authtoken' not in settings.INSTALLED_APPS
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key


class LoginCustomer(models.Model):
	class Meta:
		db_table = "login_customer"
		managed = False
	email = models.EmailField()
	first_name = models.CharField(max_length = 100)
	password = models.CharField(max_length = 255)

class DishReplacementSuggestions(models.Model):
	dietplan_food_details = models.ForeignKey(GeneratedDietPlanFoodDetails)
	food = models.ForeignKey(Food)
#	created_on = models.DateTimeField(auto_now = True)

class CustomerFoodExclusions(models.Model):
	LAMB = 'lamb_mutton'
	SEAFOOD = 'seafood'
	NUTS = 'nuts'
	WHEAT = 'wheat'
	DAIRY = 'dairy'
	POULTARY = 'poultary'
	EGG = 'egg'
	BEEF = 'beef'
	MEAT = 'meat'
	food_type_choices = (
		(LAMB , "Lamb"),
		(SEAFOOD , "Seafood"),
		(NUTS , "nuts"),
		(WHEAT , "wheat"),
		(DAIRY , "dairy"),
		(POULTARY , "poultary"),
		(EGG , "egg"),
		(BEEF , "beef"),
		(MEAT , "meat")
	)
	customer = models.ForeignKey(Customer , db_column = 'erp_customer_id')
	food_type = models.CharField(max_length = 100 , choices = food_type_choices)

	class Meta:
		managed = False
		db_table = "erp_customer_food_exclusion"

class CustomerMedicalConditions(models.Model):
	customer = models.ForeignKey(Customer , db_column = "erp_customer_id")
	condition_name = models.CharField(max_length = 50)

	class Meta:
		managed = False
		db_table = "erp_customer_medicalcondition"


class CustomerWeightRecord(models.Model):
	class Meta:
		managed = False
		db_table = "erp_customer_weight_timeline"

	customer = models.ForeignKey(Customer , db_column = "erp_customer_id")
	date = models.DateTimeField(auto_now_add = True)
	weight = models.FloatField()
	weight_type = models.IntegerField()

	@classmethod
	def latest_record(self , customer = None):
		'''
		Return the last weight update record of a customer
		'''
		if customer :
			return self.objects.filter(customer = customer).last()


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save , sender = Customer)
def create_auth_token(sender , instance = None , created = False , **kwargs):
	if created:
		Token.objects.create( user = instance )