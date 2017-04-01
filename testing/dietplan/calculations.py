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
import itertools , threading

class Calculations:
	def __init__(self , weight , height , activity , goal , exclude):
		#Assign Arguments
		self.weight = weight
		self.height = height
		self.activity = activity
		self.goal = goal
		self.exclude = exclude
		
		#calculations
		self.bmi = BMI(weight , height)
		# self.leanfactor = LeanFactor(bodyType , self.bmi.category)
		# self.bmr = BasalMetabolicRate(weight , self.leanfactor.get_lean())
		# self.tdee = TDEE(self.bmr.bmr , self.activity)
		self.ibw = IBW(self.height)
		self.calorieNumber = CalorieNumber(self.bmi , self.activity)
		self.countCalories()
		# self.makeMeals()


	def countCalories(self):
		self.calories = max( 1200 , self.ibw.ibw * self.calorieNumber.number)
		return self

	def makeMeals(self):
		self.m5 = M5(self.calories , self.goal , self.exclude).build()
		self.m3 = M3(self.calories , self.goal , self.exclude).build()
		self.m1 = M1(self.calories , self.goal , self.exclude).build()
		self.m4 = M4(self.calories , self.goal , self.exclude).build()
		self.m2 = M2(self.calories , self.goal , self.exclude).build()

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
