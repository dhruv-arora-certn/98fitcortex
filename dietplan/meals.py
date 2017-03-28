from .models import Food
from .utils import annotate_food
import heapq

class M1:
	percent = .25

	def __init__(self , calories , goal):
		self.calories_goal = calories*self.percent
		self.goal = goal
		self.marked = list(annotate_food(Food.m1_objects , self.goal))
		self.selected = []
		heapq.heapify(self.marked)

	@property
	def snack(self):
		self.snack_list = list(filter(lambda x : x.snaks , self.marked ))
		return min(self.snack_list)	

	@property
	def drink(self):
		self.drink_list = list(filter( lambda x : x.drink & x.dairy , self.marked))
		return min(self.drink_list , key = lambda x : (self.calories_goal * 0.15 - x.calorie)**2)

	def select_item(self , item):
		self.selected.append(item)
		self.marked.remove(item)
		return self

	@property
	def calories(self):
		return sum([i.calorie for i in self.selected])


class M2:
	percent = 0.15

class M3:
	percent = 0.25

class M4:
	percent = 0.15

class M5:
	percent = 0.20