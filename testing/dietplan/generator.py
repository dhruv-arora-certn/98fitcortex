from .bmi import BMI
from .lean import LeanFactor
from .bodyTypes import BodyTypes
from .bmr import BasalMetabolicRate
from .tdee import TDEE
from .goals import Goals
from .meals import M1 , M2 , M3 , M4 , M5
from .calorieNumber import CalorieNumber
from .ibw import IBW
from .calculations import Calculations
from knapsack.knapsack_dp import knapsack
import itertools , threading , lego , numpy as np

class Day:
	@lego.assemble
	def __init__(self , calculations):
		pass

	def makeMeals(self):
		self.calculations.makeMeals()

class Pipeline:
	@lego.assemble
	def __init__(self , weight , height , activity , goal , gender):
		self.excluded = []

	def Day1(self):
		print("Day 1 Exclude ," , self.exclude)
		self.day1 = Day(Calculations(self.weight , self.height , self.activity , self.goal , self.gender, self.exclude))
		self.day1.makeMeals()
		self.push_to_exclude(self.day1)

	def Day2(self):
		print("Day 2 Exclude ," , self.exclude)
		self.day2 = Day(Calculations(self.weight , self.height , self.activity , self.goal , self.gender, self.exclude))
		self.day2.makeMeals()
		self.push_to_exclude(self.day2)
	
	def Day3(self):
		print("Day 3 Exclude ," , self.exclude)
		self.day3 = Day(Calculations(self.weight , self.height , self.activity , self.goal , self.gender, self.exclude))
		self.day3.makeMeals()
		self.push_to_exclude(self.day3)
	
	def Day4(self):
		print("Day 4 Exclude ," , self.exclude)
		self.day4 = Day(Calculations(self.weight , self.height , self.activity , self.goal , self.gender, self.exclude))
		self.day4.makeMeals()
		self.push_to_exclude(self.day4)
	
	def Day5(self):
		print("Day 5 Exclude ," , self.exclude)
		self.day5 = Day(Calculations(self.weight , self.height , self.activity , self.goal , self.gender, self.exclude ))
		self.day5.makeMeals()
		self.push_to_exclude(self.day5)
	
	def Day6(self):
		print("Day 6 Exclude ," , self.exclude)
		self.day6 = Day(Calculations(self.weight , self.height , self.activity , self.goal , self.gender, self.exclude))
		self.day6.makeMeals()
		self.push_to_exclude(self.day6)
	
	def Day7(self):
		print("Day 7 Exclude ," , self.exclude)
		self.day7 = Day(Calculations(self.weight , self.height , self.activity , self.goal , self.gender, self.exclude))
		self.day7.makeMeals()
		self.push_to_exclude(self.day7)

	def push_to_exclude(self , day):
		self.excluded.append([e.name for e in day.calculations.selected if e.nuts == 0])
		self.excluded = self.excluded[-3:]
		if len(self.excluded) > 3:
			self.excluded += list(np.random.choice(self.excluded[4:] , 15  , replace = True))

	def generate(self):
		self.Day1()
		self.Day2()
		self.Day3()
		self.Day4()
		self.Day5()
		self.Day6()
		self.Day7()

	@property
	def exclude(self):
		return list(itertools.chain(*self.excluded))

