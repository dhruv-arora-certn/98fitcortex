from django.db import models

# Create your models here.
import mongoengine

mongoengine.connect(db = "98fit")

#Model Managers for Food Model
class Default(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(calarie__gt = 0)

class M1(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(m1 = '1').filter(calarie__gt = 0)

class M2(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(m2 = '1').filter(calarie__gt = 0)

class M3(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(m3 = '1').filter(calarie__gt = 0)

class M4(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(m4 = '1').filter(calarie__gt = 0)

class M5_Gain(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(m5_gain = '1').filter(calarie__gt = 0)

class M5_Loss(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(m5_loss = '1').filter(calarie__gt = 0)

class M5_Stable(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(m5_stable = '1').filter(calarie__gt = 0)


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

	@mongoengine.queryset.queryset_manager
	def m1_objects(doc_cls , queryset):
		return queryset.filter(m1 = 1).filter( calarie__gt = 0)	

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

	def update_weight(self, factor):
		self.weight *= factor
		self.update(factor)
		return self
			
	def update_quantity(self ,factor):
		self.quantity *= factor
		self.update(factor)
		return self

	def goal_nutrition(self,goal):
		return self.protein*goal.protein + self.fat*goal.fat + self.carbohydrates*goal.carbs

	class Meta:
		db_table = "business_diet_list"


class Customer(models.Model):
	first_name = models.CharField(max_length = 50)
	age = models.IntegerField()
	weight = models.CharField( max_length = 11)
	height = models.CharField( max_length = 20)
	lifestyle = models.CharField( max_length = 50)