from .bmi import BMI
from .lean import LeanFactor
from .bodyTypes import BodyTypes
from .bmr import BasalMetabolicRate
from .tdee import TDEE
from .goals import Goals

class Calculations:
	def __init__(self , weight , height , bodyType , activity , goal):
		#Assign Arguments
		self.weight = weight
		self.height = height
		self.bodyType = bodyType
		self.activity = activity
		self.goal = goal
		
		#calculations
		self.bmi = BMI(weight , height)
		self.leanfactor = LeanFactor(bodyType , self.bmi.category)
		self.bmr = BasalMetabolicRate(weight , self.leanfactor.get_lean())
		self.tdee = TDEE(self.bmr.bmr , self.activity)

		self.countCalories()

	def countCalories(self):
		self.calories = self.tdee.tdee * (1 + self.goal._diff)
		return self

	def get_m1(self):
		self.m1 = M1( self.calories , self.goal )