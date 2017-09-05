from django.db import models
from dietplan.goals import Goals
from dietplan.gender import Male , Female
from epilogue.managers import *
from django.db.models.expressions import RawSQL
from .mappers import *
from epilogue.dummyModels import *
from rest_framework import exceptions
from epilogue.utils import get_month , get_year , get_week  ,aggregate_avg , aggregate_max , aggregate_min,get_week , countBottles , countGlasses , aggregate_sum , previous_day
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from workoutplan import levels


from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

import binascii
import os
#Model Managers for Food Model

	
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
	grains_cereals = models.IntegerField()
	cereal_grains = models.IntegerField()
	salad = models.IntegerField()
	dessert = models.IntegerField()
	pulses = models.IntegerField()
	pulse = models.IntegerField()
	for_loss = models.IntegerField()
	wheat = models.IntegerField()
	lamb_mutton = models.IntegerField()
	beef = models.IntegerField()
	seafood = models.IntegerField()
	poultary = models.IntegerField()
	meat = models.IntegerField()
	egg = models.IntegerField()
	yogurt = models.IntegerField()
	pork = models.IntegerField()
	other_meat = models.IntegerField()
	nut = models.IntegerField()
	nuts = models.IntegerField()
	non_veg_gravy_items = models.IntegerField()
	vegetables = models.IntegerField()
	cuisine = models.TextField()
	calcium = models.FloatField()
	vitaminc = models.FloatField()
	iron = models.FloatField()
	image_name = models.CharField(max_length = 100)
	squared_diff_weight_loss = models.FloatField(default = 0)
	squared_diff_weight_maintain = models.FloatField(default = 0)
	squared_diff_weight_gain = models.FloatField(default = 0)
	image_name = models.CharField(max_length = 100)
	non_veg = models.IntegerField()
	
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
		print("Calling Weight" , factor)
		self.protein *= factor
		self.fat *= factor
		self.carbohydrates *= factor
		self.calarie *= factor
		self.calcium *= factor
		return self
		
	def update_weight(self, factor):
		new_weight = self.weight * factor
		new_weight = int( 5 * round(new_weight/5))
		factor = new_weight/self.weight
		self.weight = new_weight
		self.update(factor)
		return self
			
	def update_quantity(self ,factor):
		self.quantity *= factor
		self.quantity = max( 1 , round(self.quantity ))
		self.weight *= factor
		self.update(factor)
		self.weight = round( self.weight )
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
		if self.name.strip() == "Weight Loss":
			return Goals.WeightLoss
		if self.name.strip() == "Weight Gain":
			return Goals.WeightGain
		if self.name.strip() == "Muscle Gain":
			return Goals.MuscleGain
		if self.name.strip() == "Be healthy":
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
	level = models.IntegerField()
	is_authenticated = True

	def get_exclusions(self):
		q = models.Q()
		for e in self.customerfoodexclusions_set.all():
			q &= exclusionMapper.get(e.food_type , models.Q())
		q &= food_category_exclusion_mapper.get(self.food_cat , models.Q())
		return q

	@property
	def args_attrs(self):
		return [
			self.weight,
			self.height,
			self.lifestyle,
			self.goal,
			self.gender.number,
			[]
		]

	@property
	def kwargs_attrs(self):
		kwargs_attrs = {
			'exclusion_conditions' : self.get_exclusions()
		}
		return kwargs_attrs

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
			feet , inches = self.h.split('.')
			inches = 12 * float(feet) + float(inches)
			val =  inches * 0.0254
		if self.h_type == 2: #Centimeters
			val =  int(self.h)/100
		return round(val , 2)

	@property
	def weight(self):
		if int(self.w_type) == 2:
			val = float(self.w)
		if int(self.w_type) == 1:
			val = float(self.w) * 0.4536
		return round(val , 2)

	@property
	def goal(self):
		return self.objective.goal

	@property
	def gender(self):
		if self.gen.lower().strip() == "male":
			return Male
		if self.gen.lower().strip() == "female":
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
	def latest_activity(self):
		exercise_plan_count = GeneratedExercisePlan.objects.filter(customer = self).count()
		relation = ExerciseDietRelation.objects.filter(act_level = self.lifestyle).filter(fit_level = self.level).first()
		last_activity = ActivityLevelLog.latest_record(customer = self)
		if relation:
			if relation.preiodise == '1' and exercise_plan_count > 12:
				print("Relation =======> " , (relation.preiodise , exercise_plan_count , relation.uppercut))
				return relation.uppercut	
			elif last_activity and  float(last_activity.lifestyle) < float(self.lifestyle):
				print("New Activity ======>" , relation.new_activity)
				return relation.new_activity
		return float(self.lifestyle)
	
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

	def map_aggregate(self , qs , obj):
		return map( lambda x : obj(**x) , qs)

	def aggregate_sleep(self,queryset):
		field = "total_minutes"
		a = aggregate_avg(queryset , field)
		b = aggregate_min(queryset , field)
		c = aggregate_max(queryset , field)
		d = aggregate_sum(queryset , field)
		return {**a, **b,**c ,**d}


	def monthly_sleep(self , month = None , mapped = False):
		if not month:
			month = get_month()
		year = get_year()
		baseQ = self.sleep_logs.annotate(year = RawSQL("Year(start)",[])).filter(year = year)
		baseQ = baseQ.annotate(month = RawSQL("Month(start)",[])).annotate(week = RawSQL("FLOOR((DayOfMonth(start)-1)/7)+1",[])).values("week").annotate(total_minutes = models.Sum("minutes")).values("week","total_minutes")
		baseQ = baseQ.filter(month = month)	
		if mapped : 
			return self.map_aggregate(baseQ , SleepMonthly)
		return baseQ

	def monthly_sleep_aggregate(self, month = None):
		if not month:
			month = get_month()
		baseQ = self.sleep_logs.annotate(month = RawSQL("Month(start)",[])).annotate(week = RawSQL("FLOOR((DayOfMonth(start)-1)/7)+1",[])).values("week").annotate(total_minutes = models.Sum("minutes")).values("week","total_minutes")
		baseQ = baseQ.filter(month = month)
		return self.aggregate_sleep(baseQ)
	
	def weekly_sleep(self,week = None, mapped = False):
		if not week:
			week = get_week()
		year = get_year()
		baseQ = self.sleep_logs.annotate(year = RawSQL("Year(start)",[])).filter(year = year)
		baseQ = self.sleep_logs.annotate(week = RawSQL("Week(start)",[])).filter(week = week).annotate(day = RawSQL("weekday(start)+1",[])).values("day").annotate(total_minutes = models.Sum("minutes")).values("day","total_minutes")
		if mapped:
			return self.map_aggregate(baseQ , SleepWeekly )
		return baseQ
		
	def weekly_sleep_aggregated(self , week = None):
		if not week:
			week = get_week()
		baseQ = self.sleep_logs.annotate(week = RawSQL("Week(start)",[])).annotate(day = RawSQL("weekday(start)+1",[])).values("day").annotate(total_minutes = models.Sum("minutes")).values("day", "total_minutes")
		baseQ = baseQ.filter(week = week)
		return self.aggregate_sleep(baseQ)

	
	def monthly_water(self,month = None):
		if not month:
			month = get_month()
		baseQ = self.water_logs.annotate(month = RawSQL("Month(added)",[])).filter(month = month).annotate(week = RawSQL("Week(added)",[])).values("week").annotate(total_quantity = models.Sum(models.F("quantity")*models.F("count")))	
		baseQ = countBottles(baseQ)
		baseQ = countGlasses(baseQ)
		return baseQ

	def weekly_water(self , week = None):
		if not week:
			week = get_week()
		baseQ = self.water_logs.annotate(day = RawSQL("weekday(added)+1",[])).annotate(week = RawSQL("Week(added)",[])).filter(week = week).values("day").annotate(total_quantity = models.Sum(models.F("quantity")*models.F("count")))
		baseQ = countBottles(baseQ)
		baseQ = countGlasses(baseQ)
		return baseQ

	def last_day_sleep(self):
		day = previous_day()
		baseQ = self.sleep_logs.annotate(date = RawSQL("date(start)",[])).filter(date = day).values("date").annotate(total_minutes = models.Sum("minutes")).values("total_minutes" , "date" , "end" , "start").first()
		return baseQ

	def weekly_activity(self,week = None):
		if not week:
			week =  get_week()
		year = get_year()
		baseQ = self.activity_logs.annotate(day = RawSQL("weekday(start)+1",[])).annotate(year = RawSQL("Year(start)",[])).filter(year = year).annotate(week = RawSQL("Week(start)",[])).filter(week = week)
		baseQ = baseQ.values("day").annotate(total_cals = models.Sum("cals")).annotate(total_distance = models.Sum("distance")).annotate(total_steps = models.Sum("steps")).annotate(total_duration = models.Sum("duration")).order_by("-end")
		baseQ = baseQ.values("day" , "total_cals" , "total_steps" , "total_distance" , "total_duration")
		return baseQ

	def monthly_activity(self,month = None):
		if not month:
			month = get_month()
		year = get_year()

		baseQ = self.activity_logs.annotate(month = RawSQL("Month(start)",[])).annotate(year = RawSQL("Year(start)",[])).annotate(week = RawSQL("FLOOR((DayOfMonth(start)-1)/7)+1",[])).filter(month = month)
		baseQ = baseQ.values("week").annotate(total_cals = models.Sum("cals")).annotate(total_distance = models.Sum("distance")).annotate(total_steps = models.Sum("steps")).annotate(total_duration = models.Sum("duration"))
		baseQ = baseQ.values("week" , "total_cals" , "total_steps" , "total_distance" , "total_duration")
		return baseQ

	@property
	def level_obj(self):
		if self.level == 1:
			return levels.Novice
		elif self.level == 2:
			return levels.Beginner
		elif self.level == 3:
			return levels.Intermediate
		return levels.Novice
				
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

	customer = models.ForeignKey(Customer , db_column = "erp_customer_id" , related_name = "dietplans")
	created_on = models.DateTimeField(auto_now_add = True)
	user_week_id = models.IntegerField(default = 1)
	week_id = models.IntegerField(default = 1)
	company_id = models.IntegerField(default = 0)
	plan_type = models.CharField(max_length = 50 , default = "system generated plan")
	medi_applicable = models.CharField(max_length = 20 , default = "")
	year = models.IntegerField()
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
		max_day = baseQ.aggregate(models.Max('day')).get("day__max") or 7
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
			float(self.customer.latest_activity),
			self.customer.goal,
			self.customer.gender.number,
			user = self.customer,
			dietplan = self,
			persist = True
		)
		self.pipeline.regenerate()

	@property
	def items(self):
		return list(self.meals.values_list("food_name" , flat = True))

class GeneratedDietPlanFoodDetails(models.Model):
	'''
	Store the generated diet plan of a day here
	'''
	class Meta:
		managed = False
		db_table = "erp_diet_plan_food_details"

	dietplan = models.ForeignKey(GeneratedDietPlan , db_column = "erp_diet_plan_id"  , related_name = "meals") 
	food_item = models.ForeignKey(Food , db_column = "business_diet_list_id")
	food_name = models.CharField(max_length = 255)
	meal_type = models.CharField(max_length = 20)
	day = models.IntegerField()
	calorie = models.CharField(max_length = 50)
	weight = models.FloatField(default = 0)
	quantity = models.FloatField(default = 0)
	food_type = models.CharField(max_length = 50)
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
		f = f.filter(fruit = item.fruit).filter(drink = item.drink).filter(dairy = item.dairy).filter(snaks = item.snaks).filter(vegetable = item.vegetable).filter(grains_cereals = item.grains_cereals).filter(salad = item.salad).filter(yogurt = item.yogurt).filter(dessert=  item.dessert).filter(pulses = item.pulses).filter(cuisine = item.cuisine).filter(nuts = item.nuts).filter(nut = item.nut)
		f = f.filter(self.dietplan.customer.get_exclusions())
		f = f.filter(self.getMealRestrictions())
		f = f.annotate(d = RawSQL("Abs(%s - %s)" , [field , getattr(self.food_item,field)])).exclude(id = self.food_item_id).order_by("d").order_by(field).first()
		print("Old item" , self.food_item)
		print("New item" , f)
		if not f:
			#If previous suggestions exist , cycle them
			return self

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

		return self.food_item

	@property
	def old_suggestions(self):
		return list(self.suggestions.values_list('food__name' , flat = True))

	def update_attrs(self , item):
		self.calorie = str(item.calarie)
		self.weight = item.weight
		self.quantity = item.quantity
		self.size = item.size
		self.food_name = item.name
		return self

	def getMealRestrictions(self):
		if self.meal_type == "m4":
			if self.food_item.fruit == 1:
				return ~models.Q(name__contains = "Handful")
		return models.Q()

	def otherDishesFromMeal(self):
		return GeneratedDietPlanFoodDetails.objects.filter(dietplan = self.dietplan).filter(meal_type = self.meal_type).filter(day = self.day).exclude(id = self.id)

class GeneratedExercisePlan(models.Model):
	class Meta:
		db_table = "erp_exercise_plan"
		managed = False
	
	customer = models.ForeignKey(Customer , db_column = "erp_customer_id")
	created_on = models.DateTimeField(default = None)
	glo_level_id = models.IntegerField()

class ActivityLevelLog(models.Model):
	class Meta:
		managed = False
		db_table = "relation_log"
	customer = models.ForeignKey(Customer , db_column = "erp_customer_id")
	lifestyle = models.CharField(max_length = 50)	
	
	@property
	def activity(self):
		return float(self.lifestyle)

	@classmethod
	def latest_record(self , customer = None):
		if customer:
			return self.objects.filter(customer = customer).last()

class ExerciseDietRelation(models.Model):
	class Meta:
		managed = False
		db_table = "relation_ep_dp"
	act_level = models.CharField(max_length = 150)
	fit_level = models.CharField(max_length = 150)
	new_act_lavel = models.CharField(max_length = 150)
	preiodise = models.IntegerField()
	uppercut = models.CharField(max_length = 30)

	@property
	def activity(self):
		return float(self.act_level)

	@property
	def fitness(self):
		return float(self.fit_level)

	@property
	def new_activity(self):
		return float(self.new_act_lavel)

	@property
	def uppercut_level(self):
		return float(self.uppercut) 


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
	customer = models.OneToOneField(Customer , db_column = "erp_customer_id")

class DishReplacementSuggestions(models.Model):
	dietplan_food_details = models.ForeignKey(GeneratedDietPlanFoodDetails , related_name = "suggestions")
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

	def __str__(self):
		return self.condition_name

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

class FoodTypeSizes(models.Model):
	class Meta:
		managed = False
		db_table = "food_type_sizes"
	size = models.CharField(max_length = 50)
	weight = models.IntegerField()
	type = models.CharField(max_length = 50)

@receiver(post_save , sender = Customer)
def create_auth_token(sender , instance = None , created = False , **kwargs):
	if created:
		Token.objects.create( user = instance )

class WaterContainer(models.Model):
	Bottle = "bottle"
	Glass = "glass" 
	choices = [
		(Bottle , "Bottle"),
		(Glass , "Glass")
	]
	name = models.CharField(max_length = 20 , choices = choices)

class CustomerWaterLogs(models.Model):
	saved = models.DateTimeField(auto_now_add = True)
	count = models.IntegerField()
	customer = models.ForeignKey(Customer, related_name = "water_logs")
	container = models.ForeignKey(WaterContainer)
	quantity = models.IntegerField()
	added = models.DateTimeField(null = True)	

	class Meta:
		indexes = [
			models.Index(fields = ['customer_id']),
			models.Index(fields = ['container'])
		]
	@property
	def total(self):
		return self.quantity * self.count
	
	def aggregate_monthly(self , month):
		pass

class CustomerSleepLogs(models.Model):
	class Meta:
		db_table = "user_sleep_logs"
		managed = False
	start = models.DateTimeField(auto_now = False)
	end = models.DateTimeField(auto_now = False)
	minutes = models.IntegerField()
	customer = models.ForeignKey(Customer , db_column = "erp_customer_id" , related_name = "sleep_logs")
	saved = models.DateTimeField(auto_now_add = True)

class CustomerActivityLogs(models.Model):
	timestamp = models.DateTimeField(null = True)
	steps = models.IntegerField()
	cals = models.IntegerField()
	customer = models.ForeignKey(Customer , related_name = "activity_logs", db_column = "erp_customer_id")
	duration = models.IntegerField()
	start = models.DateTimeField(auto_now = False)
	end = models.DateTimeField(auto_now = False)
	distance = models.IntegerField()
