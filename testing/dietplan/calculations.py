from .bmi import BMI
from .lean import LeanFactor
from .bodyTypes import BodyTypes
from .bmr import BasalMetabolicRate
from .tdee import TDEE
from .goals import Goals
from .meals import M1 , M2 , M3 , M4 , M5
from .calorieNumber import CalorieNumber
from .ibw import IBW
from knapsack.knapsack_dp import knapsack
import itertools , threading , lego

class Calculations:
	@lego.assemble
	def __init__(self , weight , height , activity , goal , gender,  exclude):
		#calculations
		self.bmi = BMI(weight , height)
		self.ibw = IBW(self.height, self.gender)
		self.calorieNumber = CalorieNumber(self.bmi , self.activity)
		self.countCalories()


	def countCalories(self):
		self.calories = max( 1200 , self.ibw.ibw * self.calorieNumber.number)
		return self

	def makeMeals(self):
		self.m5 = M5(self.calories , self.goal , exclude = self.exclude)
		self.m5.build()
		self.m3 = M3(self.calories , self.goal , exclude = self.exclude + [e.name for e in self.m5.selected] , extra = self.m5.calories_remaining)
		self.m3.build()
		self.m1 = M1(self.calories , self.goal , exclude = self.exclude + [e.name for e in self.m3.selected+self.m5.selected], extra = self.m3.calories_remaining)
		self.m1.build()
		self.m4 = M4(self.calories , self.goal , exclude = self.exclude + [e.name for e in self.m3.selected+self.m5.selected+self.m1.selected], extra = self.m1.calories_remaining)
		self.m4.build()
		self.m2 = M2(self.calories , self.goal , exclude = self.exclude + [e.name for e in self.m3.selected+self.m5.selected+self.m1.selected+self.m4.selected], extra = self.m4.calories_remaining)
		self.m2.build()

	def get_m1(self):
		self.m1 = M1( self.calories , self.goal )

	@property
	def selected(self):
		return list(itertools.chain(*[self.m1.selected, self.m3.selected , self.m5.selected , self.m4.selected , self.m2.selected]))

	@property
	def protein(self):
		return sum([i.protein for i in self.selected])

	@property
	def carbs(self):
		return sum([i.carbohydrates for i in self.selected])

	@property
	def fat(self):
		return sum([i.fat for i in self.selected])

	@property
	def calories_achieved(self):
		return self.m1.calories + self.m3.calories + self.m5.calories + self.m2.calories + self.m4.calories

	@property
	def protein_ideal(self):
		return (self.goal.protein * self.calories)/4

	@property
	def carbs_ideal(self):
		return (self.goal.carbs * self.calories) / 4

	@property
	def fat_ideal(self):
		return (self.goal.fat * self.calories) /  9

	@property
	def random(self):
		return [e.name for e in self.m1.random() +self.m2.random() +self.m3.random() +self.m4.random() +self.m5.random()] 
