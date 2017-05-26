from django.db import models
from dietplan.goals import Goals
from dietplan.gender import Male , Female
from epilogue.managers import *
from django.db.models.expressions import RawSQL
#Model Managers for Food Model

fieldMapper = {
		Goals.WeightLoss : "squared_diff_weight_loss",
		Goals.MaintainWeight : "squared_diff_weight_maintain",
		Goals.WeightGain : "squared_diff_weight_gain",
		Goals.MuscleGain : "squared_diff_muscle_gain"
}

class Food(models.Model):
	name = models.TextField()
	quantity = models.IntegerField()
	calarie = models.FloatField()
	serving = models.TextField()
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
	cuisine = models.TextField()
	nuts = models.IntegerField()
	calcium = models.FloatField()
	vitaminc = models.FloatField()
	iron = models.FloatField()
	image_name = models.CharField(max_length = 100)
	squared_diff_weight_loss = models.FloatField(default = 0)
	squared_diff_weight_maintain = models.FloatField(default = 0)
	squared_diff_weight_gain = models.FloatField(default = 0)

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
		self.update(factor)
		return self

	def goal_nutrition(self,goal):
		return self.protein*goal.protein + self.fat*goal.fat + self.carbohydrates*goal.carbs

	@property
	def image(self):
		return "https://s3-ap-southeast-1.amazonaws.com/98fitasset/image/diet/%s"%(self.image_name)

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

	email = models.CharField(max_length = 255)
	first_name = models.CharField(max_length = 25, blank = True)
	last_name = models.CharField(max_length = 25 , blank = True , null = True)
	create_on = models.DateTimeField(auto_now_add = True)
	mobile = models.CharField(max_length = 11 , blank = True , null = True)
	age = models.IntegerField()
	w = models.CharField(db_column = "weight", max_length = 11)
	h = models.CharField(db_column = "height", max_length = 20)
	ls = models.CharField( max_length = 50 , db_column = "lifestyle")
	objective = models.ForeignKey(Objective , db_column = "objective")
	gen = models.CharField(max_length = 20 , db_column = "gender")

	is_authenticated = True
	@property
	def plans(self):
		return {
			e.week_id : e.dayWisePlan for e in self.generateddietplan_set.all()
		}

	@property
	def height(self):
		return float(self.h)*0.3048

	@property
	def weight(self):
		return float(self.w)

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
	def is_active(self):
		return True
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



class GeneratedDietPlanFoodDetails(models.Model):
	'''
	Store the generated diet plan of a day here
	'''
	class Meta:
		managed = False
		db_table = "erp_diet_plan_food_details"

	dietplan = models.ForeignKey(GeneratedDietPlan , db_column = "erp_diet_plan_id") 
	food_item = models.ForeignKey(Food , db_column = "business_diet_list_id")
	food_name = models.CharField(max_length = 255)
	meal_type = models.CharField(max_length = 20)
	day = models.IntegerField()
	calorie = models.CharField(max_length = 50)
	weight = models.FloatField(default = 0)
	quantity = models.FloatField(default = 0)

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

	def find_closest(self, *args):
		'''
		*args represent the additional arguments that might be required in futurej
		'''
		goal = self.dietplan.customer.goal
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
		f = f.filter(fruit = item.fruit).filter(drink = item.drink).filter(dairy = item.dairy).filter(snaks = item.snaks).filter(vegetable = item.vegetable).filter(cereal_grains = item.cereal_grains).filter()
		f = f.annotate(d = RawSQL("Abs(%s - %s)" , [field , getattr(self,field)])).order_by("d").filter()[:5]


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