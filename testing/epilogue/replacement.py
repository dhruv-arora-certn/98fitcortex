from django.db import models
from dietplan import meals
from epilogue.models import *
from dietplan.calculations import Calculations
import lego
import inspect

mealMapper = {
	'm1' : meals.M1,
	'm2' : meals.M2,
	'm3' : meals.M3,
	'm4' : meals.M4,
	'm5' : meals.M5
}
class PseudoMeal():

	@lego.assemble
	def __init__(self , dish , exclude , selected = None ,  replaceMeal = False):
		del self.selected
		self._meal_type = mealMapper.get(dish.meal_type)
		self.dish = dish
		self._user = self.dish.dietplan.customer
		self.exclude = exclude
		self.calculations = Calculations(
			*self._user.args_attrs,
			**self._user.kwargs_attrs
		)
		self.replaceMeal = replaceMeal
		self.calories = self.calculations.calories
		self._selected = selected 
		self.argMapper = {
			'calories' : self._get_calories(),
			'disease' : None,
			'exclude' : self._get_exclude(),
			'exclude2' : self._get_exclude2(),
			'exclusion_conditions' : self._get_exclusion_conditions(),
			'extra' : 0,
			'goal' : self._user.goal,
			'make_combination' : self._get_make_combination(),
			'make_dessert' : self._get_make_dessert(),
			'selected' : self._get_selected()[self.dish.meal_type]
		}
		self.meal = self._meal_type(
			**self.getMealArgs()
		)

	def build(self):
		if self.replaceMeal:
			self.meal.build()
		else:
			func = self.meal.buildMapper.get(self.dish.food_type)
			func()

	def getMealArgs(self):
		args = inspect.signature(self._meal_type)
		args_dict = {}
		for e in args.parameters:
			args_dict.update({
				e : self.argMapper[e]
			})
		return args_dict
	
	def save(self):
		pass

	def _get_calories(self):
		return 	self.calories
	
	def _get_disease(self):
		return None
	
	def _get_exclude(self):
		return self.exclude
	
	def _get_exclude2(self):
		return None
	
	def _get_exclusion_conditions(self):
		return self._user.get_exclusions()
	
	def _get_extra(self):
		return 0
	
	def _get_make_combination(self):
		return self.dish.food_type == "combination"
	
	def _get_make_dessert(self):
		return self.dish.food_type == "dessert"

	def _get_selected(self):
		return self._selected

class ReplacementPipeline():
	'''
	Pipeline for regenerating a dish/meal.
	'''
	@lego.assemble
	def __init__(self , dish = None ,replaceMeal = False):
		self._user = self.dish.dietplan.customer
		if replaceMeal:
			baseQ = GeneratedDietPlanFoodDetails.objects.filter(dietplan__id = self.dish.dietplan.id).filter(day = self.dish.day).filter(meal_type = self.dish.meal_type).exclude(id = self.dish.id)
			self.other_dishes = baseQ
			self.other_dishes_dict = {
				e.food_type : e for e in baseQ
			}
		self.dietplan_id = self.dish.dietplan.id
		self.day = self.dish.day
		self.meal_type = self.dish.meal_type
		self._selected = self.getSelected()
		self.meal = self.intializeMeal()


	def intializeMeal(self):
		return PseudoMeal(self.dish , self.get_initial_exclude() , selected = self._selected ,replaceMeal = True) 

	def get_initial_exclude(self , days = 4):
		items = []
		last_plan = GeneratedDietPlan.objects.filter(customer = self._user).last()
		if last_plan:
			items = last_plan.get_last_days(days)
		items.extend(self.get_same_day_exclude())
		items.extend(self.get_suggestions_exclude())
		return items

	def get_suggestions_exclude(self):
		items = list(self.dish.suggestions.values_list("food__name", flat = True))
		if self.replaceMeal:
			for e in self.other_dishes:
				items.extend(e.suggestions.values_list("food__name" , flat = True)[:5])
		return items

	def get_same_day_exclude(self):
		baseQ = GeneratedDietPlanFoodDetails.objects.filter(dietplan__id = self.dish.dietplan.id).filter(day = self.dish.day).exclude(meal_type = self.dish.meal_type)
		items = baseQ.values_list('food_name' , flat = True)
		return items

	def getSelected(self):
		baseQ = GeneratedDietPlanFoodDetails.objects.filter(dietplan__id = self.dish.dietplan.id).exclude(id = self.dish.id).filter(day = self.dish.day)
		if self.replaceMeal:
			return {
				self.dish.meal_type : {}
			}
		else:
			baseQ = baseQ.filter(meal_type = self.dish.meal_type)
		d = {  
			self.dish.meal_type : {
				e.food_type : e.food_item.update(e.factor) for e in baseQ
				}
			}
		return d
	
	def save(self):
		self.created = {}
		if self.replaceMeal:
			for e,f in self._selected.get(self.dish.meal_type).items():
				c = GeneratedDietPlanFoodDetails.objects.create(
					dietplan = self.dietplan_id,
					food_item  = f,
					food_name = f.name,
					food_type = e,
					day = self.day,
					meal_type = self.meal_type,
					calorie = str(f.calarie),
					weight = f.weight,
					quantity = f.quantity,
					size = f.size
				)
				self.created.update({e:c})
			self.dish.delete()
			[e.delete() for e in self.other_dishes]
		else:
			pass
			
	@property
	def selected(self):
		return list(self._selected.get(self.dish.meal_type).values())

	@property
	def replacement(self):
		return self._selected.get(self.dish.meal_type).get(self.dish.food_type)