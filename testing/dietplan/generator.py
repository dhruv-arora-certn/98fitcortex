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
from epilogue.models import Food , GeneratedDietPlan , GeneratedDietPlanFoodDetails
from epilogue.utils import get_day , get_week
import itertools , threading , lego , numpy as np , click
from datetime import datetime
from django.db.models import Q
from numpy.random import choice


class Day:
	@lego.assemble
	def __init__(self , calculations , day = None , persist = False , dietplan = None , comboDays = None):
		pass

	def makeMeals(self):
		self.calculations.makeMeals()
		self.persist_db()

	def makeMeal(self , meal = None):
		assert meal
		newMeal = self.calculations.makeMeal(meal)

	def persist_db(self):
		print("&&&&&& "  ,self.persist , self.day , self.dietplan)
		if self.persist and self.day and self.dietplan:
			self.generated = []
			for m in self.calculations.meals:	
				for e in m.selected:
					print("Pushing Day to DB")
					obj = GeneratedDietPlanFoodDetails.objects.create(dietplan = self.dietplan , food_item = e , food_name = e.name , day = self.day , meal_type = m.__class__.__name__.lower() , calorie = str(e.calarie)  , weight = e.weight , quantity = e.quantity , size = e.size)
					self.generated.append(obj)

class Pipeline:
	@lego.assemble
	def __init__(self , weight , height , activity , goal , gender , user = None ,disease = None , persist = False , week = None , dietplan = None):
		self.excluded = []
		if self.week is None:
			week = get_week(datetime.today())
		user_week = 1
		
		self.exclusion_conditions = Q()	
		if self.user:
			user_week = week - get_week(user.create_on) + 1
			self.excluded = [self.get_initial_exclude()]
			self.excluded2 = None
			self.exclusion_conditions = self.user.get_exclusions()
			if ('wheat',0) in self.exclusion_conditions.children:
				self.excluded2 = [self.get_initial_exclude(days = 2)]

		if self.dietplan:
			self._is_dietplan_set = True
		if self.persist and self.user and not self.dietplan:
			self.dietplan = GeneratedDietPlan.objects.create(customer = user , week_id = week , user_week_id = user_week)

		self.comboDays = self.daysForCombinations()
		self.dessertDays = self.getDessertDays()

	def daysForCombinations(self):
		l = [e for e in range(1,8)]
		m3 = choice(
			l,
			size = 2,
			replace = True,
			p = [1/7 for _ in range(7)]
		)
		#Remove elements from list
		try: 
			print("M3" , m3)
			[l.remove(e) for e in m3]
			print("L" , l)
		except Exception as e:
			# import ipdb
			# ipdb.set_trace()
			pass
		m5 = choice(
			l,
			size = 1,
			replace = True,
			p = [1/5 for _ in range(5)]
		)
		return {
			'3' : m3,
			'5' : m5
		}

	def getDessertDays(self):

		if self.user.goal == Goals.WeightLoss:
			size = 1
		else:
			size = 2

		l = [e for e in range(1,8)]
		dessert = choice(
			l , 
			size = size,
			p = [1/7 for _ in range(7)]
		)
		return dessert

	def get_initial_exclude(self , days = 4):
		'''
		Initialize the list of excluded items from the past 3 days and user's food preferences
		'''
		items = []
		last_plan = GeneratedDietPlan.objects.filter( customer = self.user ).last()
		if last_plan:
			items = last_plan.get_last_days(days)

		return items 
	
	def Day1(self):
		print("Day 1 Exclude ," , self.exclude)
		self.day1 = Day(
			Calculations(self.weight ,
			 self.height ,
			 self.activity ,
			 self.goal ,
			 self.gender,
			 self.exclude ,
			 disease = self.disease ,
			 exclusion_conditions = self.exclusion_conditions ,
			 exclude2 = self.excluded2,
			 comboDays = {
			 	'm3' : 1 in self.comboDays.get('3'),
			 	'm5' : 1 in self.comboDays.get('5')
			 },
			 dessertDays = 1 in self.dessertDays
			), 
			persist = self.persist, 
			dietplan = self.dietplan,
			day = "1")
		self.day1.makeMeals()
		self.push_to_exclude(self.day1)

	def Day2(self):
		print("Day 2 Exclude ," , self.exclude)
		self.day2 = Day(
			Calculations(self.weight ,
			 	self.height ,
			 	self.activity ,
			 	self.goal ,
			 	self.gender,
			 	self.exclude ,
			 	disease = self.disease ,
			 	exclusion_conditions = self.exclusion_conditions ,
			 	exclude2 = self.excluded2 ,
				comboDays = {
			 	'm3' : 2 in self.comboDays.get('3'),
			 	'm5' : 2 in self.comboDays.get('5')
			 }, 
			 dessertDays = 2 in self.dessertDays
			), 
			persist = self.persist, 
			dietplan = self.dietplan,
			day = "2"
		)
		self.day2.makeMeals()
		self.push_to_exclude(self.day2)
	
	def Day3(self):
		print("Day 3 Exclude ," , self.exclude)
		self.day3 = Day(
			Calculations(self.weight ,
			 self.height ,
			 self.activity ,
			 self.goal ,
			 self.gender,
			 self.exclude ,
			 disease = self.disease ,
			 exclusion_conditions = self.exclusion_conditions , 
			 exclude2 = self.excluded2 ,
			comboDays = {
			 	'm3' : 3 in self.comboDays.get('3'),
			 	'm5' : 3 in self.comboDays.get('5')
			 },
			 dessertDays = 3 in self.dessertDays
			), 
			persist = self.persist, 
			dietplan = self.dietplan,
			day = "3"
		)
		self.day3.makeMeals()
		self.push_to_exclude(self.day3)
	
	def Day4(self):
		print("Day 4 Exclude ," , self.exclude)
		self.day4 = Day(
			Calculations(self.weight ,
			 self.height ,
			 self.activity ,
			 self.goal ,
			 self.gender,
			 self.exclude ,
			 disease = self.disease ,
			 exclusion_conditions = self.exclusion_conditions ,
			 exclude2 = self.excluded2 ,
			 comboDays = {
			 	'm3' : 4 in self.comboDays.get('3'),
			 	'm5' : 4 in self.comboDays.get('5')
			 },
			 dessertDays = 4 in self.dessertDays
			), 
			persist = self.persist, 
			dietplan = self.dietplan,
			day = "4"
		)
		self.day4.makeMeals()
		self.push_to_exclude(self.day4)
	
	def Day5(self):
		print("Day 5 Exclude ," , self.exclude)
		self.day5 = Day(
			Calculations(self.weight ,
			 self.height ,
			 self.activity ,
			 self.goal ,
			 self.gender,
			 self.exclude ,
			 disease = self.disease ,
			 exclusion_conditions = self.exclusion_conditions ,
			 exclude2 = self.excluded2 ,
			 comboDays = {
			 	'm3' : 5 in self.comboDays.get('3'),
			 	'm5' : 5 in self.comboDays.get('5')
			 },
			 dessertDays = 5 in self.dessertDays
			 ), 
			persist = self.persist,
			dietplan = self.dietplan,
			day = "5"
		)
		self.day5.makeMeals()
		self.push_to_exclude(self.day5)
	
	def Day6(self):
		print("Day 6 Exclude ," , self.exclude)
		self.day6 = Day(
			Calculations(self.weight ,
				self.height ,
				self.activity ,
				self.goal ,
				self.gender,
				self.exclude ,
				disease = self.disease ,
				exclusion_conditions = self.exclusion_conditions ,
				exclude2 = self.excluded2 ,
				comboDays = {
			 	'm3' : 6 in self.comboDays.get('3'),
			 	'm5' : 6 in self.comboDays.get('5')
			 },
			 dessertDays = 6 in self.dessertDays
			), 
			persist = self.persist, 
			dietplan = self.dietplan,
			day = "6"
		)
		self.day6.makeMeals()
		self.push_to_exclude(self.day6)
	
	def Day7(self):
		print("Day 7 Exclude ," , self.exclude)
		self.day7 = Day(
			Calculations(self.weight ,
			 self.height ,
			 self.activity ,
			 self.goal ,
			 self.gender,
			 self.exclude ,
			 disease = self.disease ,
			 exclusion_conditions = self.exclusion_conditions ,
			 exclude2 = self.excluded2 ,
			 comboDays = {
			 	'm3' : 7 in self.comboDays.get('3'),
			 	'm5' : 7 in self.comboDays.get('5')
			 } ,
			 dessertDays = 7 in self.dessertDays
			), 
			persist = self.persist, 
			dietplan = self.dietplan,
			day = "7"
		)
		self.day7.makeMeals()
		self.push_to_exclude(self.day7)

	def push_to_exclude(self , day):
		self.excluded.append([e.name for e in day.calculations.selected if e.nuts == 0])
		self.excluded = self.excluded[-3:]
		if len(self.excluded) > 3:
			self.excluded += list(np.random.choice(self.excluded[4:] , 15  , replace = True))

	def generate(self , day = None):
		#If it is the present week
		if not day:
			days = range(1,8)
		else :
			days = [day]
			
		for e in days:
			getattr(self , "Day"+str(e))()

	@property
	def exclude(self):
		return list(itertools.chain(*self.excluded))

	def show_calcium(self):
		click.secho( "Day 1: %s mg" % self.day1.calculations.calcium  , fg = "green" if self.day1.calculations.calcium > 800 and self.day1.calculations.calcium < 1050 else "red" )
		click.secho( "Day 2: %s mg" % self.day2.calculations.calcium  , fg = "green" if self.day2.calculations.calcium > 800 and self.day2.calculations.calcium < 1050 else "red" )
		click.secho( "Day 3: %s mg" % self.day3.calculations.calcium  , fg = "green" if self.day3.calculations.calcium > 800 and self.day3.calculations.calcium < 1050 else "red" )
		click.secho( "Day 4: %s mg" % self.day4.calculations.calcium  , fg = "green" if self.day4.calculations.calcium > 800 and self.day4.calculations.calcium < 1050 else "red" )
		click.secho( "Day 5: %s mg" % self.day5.calculations.calcium  , fg = "green" if self.day5.calculations.calcium > 800 and self.day5.calculations.calcium < 1050 else "red" )
		click.secho( "Day 6: %s mg" % self.day6.calculations.calcium  , fg = "green" if self.day6.calculations.calcium > 800 and self.day6.calculations.calcium < 1050 else "red" )
		click.secho( "Day 7: %s mg" % self.day7.calculations.calcium  , fg = "green" if self.day7.calculations.calcium > 800 and self.day7.calculations.calcium < 1050 else "red" )

	def sum_property(self , property):
		l = [
			self.day1.calculations , self.day2.calculations , self.day3.calculations, self.day4.calculations , self.day5.calculations , self.day6.calculations , self.day7.calculations
		]
		return sum( getattr(i , property) for i in l)

	def regenerate(self):
		#Saving the old food details. These will be deleted on successful generation of diet plan
		self._old = list(GeneratedDietPlanFoodDetails.objects.filter(dietplan__id = self.dietplan.id).all())
		# generate() automatically uses the class attributes to pass to each day
		self.generate()

		self._new = list(GeneratedDietPlanFoodDetails.objects.filter(dietplan__id = self.dietplan.id).exclude(id__in = [e.id for e in self._old]))

		#Deleting old assigned meals
		if self._new:
			[e.delete() for e in self._old]


