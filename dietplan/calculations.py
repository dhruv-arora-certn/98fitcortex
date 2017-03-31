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
import itertools

class Calculations:
	def __init__(self , weight , height , bodyType , activity , goal , exclude):
		#Assign Arguments
		self.weight = weight
		self.height = height
		self.bodyType = bodyType
		self.activity = activity
		self.goal = goal
		self.exclude = exclude
		
		#calculations
		self.bmi = BMI(weight , height)
		self.leanfactor = LeanFactor(bodyType , self.bmi.category)
		self.bmr = BasalMetabolicRate(weight , self.leanfactor.get_lean())
		self.tdee = TDEE(self.bmr.bmr , self.activity)
		self.ibw = IBW(self.height)
		self.calorieNumber = CalorieNumber(self.bmi , self.activity)
		self.countCalories()
		self.makeMeals()


	def countCalories(self):
		self.calories = self.ibw.ibw * self.calorieNumber.number
		return self

	def makeMeals(self):
		self.m5 = M5(self.calories , self.goal , self.exclude).build()
		self.m3 = M3(self.calories , self.goal , self.exclude).build()
		self.m1 = M1(self.calories , self.goal , self.exclude).build()

	def get_m1(self):
		self.m1 = M1( self.calories , self.goal )

	@property
	def selected(self):
		return list(itertools.chain(*[self.m1.selected, self.m3.selected , self.m5.selected]))

	@property
	def protein(self):
		return sum([i.protein for i in self.selected])

	@property
	def carbs(self):
		return sum([i.carbohydrates for i in self.selected])

	@property
	def fat(self):
		return sum([i.fat for i in self.selected])
