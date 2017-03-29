from .models import Food
from .utils import annotate_food
from .goals import Goals
from knapsack.knapsack_dp import knapsack,display
import heapq

class Base:

	def select_item(self , item):
		self.selected.append(item)
		self.marked.remove(item)
		return self

	@property
	def calories(self):
		return sum([i.calorie for i in self.selected])

	@property
	def calories_remaining(self):
		return self.calories_goal - self.calories

class M1(Base):
	percent = .25

	def __init__(self , calories , goal , exclude=  ""):
		self.calories_goal = calories*self.percent
		self.goal = goal
		self.queryset = Food.m1_objects.filter(name__ne = exclude)
		if goal == Goals.WeightLoss : 
			self.queryset.filter(for_loss = 1).all()
		
		self.marked = list(annotate_food(self.queryset , self.goal))
		self.selected = []
		# heapq.heapify(self.marked)

	def allocate_restrictions(self):
		self.select_item(self.drink)
		self.remove_drinks()
		self.select_item(Food.m1_objects.filter(name = "Boiled Egg White").first())
	def pop_snack(self):
		self.snack_list = list(filter(lambda x : x.snaks , self.marked ))
		heapq.heapify(self.snack_list)
		return heapq.heappop(self.snack_list)	

	@property
	def drink(self):
		self.drink_list = list(filter( lambda x : x.drink & x.dairy , self.marked))
		# self.marked = list(set(self.marked) - set(self.drink_list))
		return min(self.drink_list , key = lambda x : (self.calories_goal * 0.15 - x.calorie)**2)

	def remove_drinks(self):
		self.marked = list(set(self.marked) - set(self.drink_list))
		return self
	

	def build(self):
		self.allocate_restrictions()
		calories = self.calories_remaining
		food_list = list(filter( lambda x : bool(x.snaks) , self.marked))
		F,test = knapsack(food_list , calories)
		items = display(F , calories , food_list)
		# import ipdb
		# ipdb.set_trace()
		self.snacks = [food_list[i] for i in items]
		[self.select_item(i) for i in self.snacks]
		return self


class M2:
	percent = 0.15

class M3(Base):
	percent = 0.25

	def __init__(self , calories , goal , exclude = "" , yogurt = True):
		self.calories_goal = calories*self.percent
		self.goal = goal
		self.queryset = Food.m3_objects.filter(salad = 0).filter(name__ne = exclude)
		self.yogurt = yogurt
		self.marked = list(annotate_food(self.queryset , self.goal))
		self.selected = []
		# heapq.heapify(self.marked)

	def select_yogurt(self):
		calories = 0.15*self.calories_goal
		food_list = list(filter( lambda x : bool(x.yogurt) , self.marked))
		F,test = knapsack(food_list , calories)
		items = display(F , calories , food_list)
		# import ipdb
		# ipdb.set_trace()
		self.yogurt = [food_list[i] for i in items]
		[self.select_item(i) for i in self.yogurt]

	def select_dessert(self):
		calories = 0.12*self.calories_goal
		food_list = list(filter( lambda x : bool(x.dessert) , self.marked))
		F,test = knapsack(food_list , calories)
		items = display(F , calories , food_list)
		# import ipdb
		# ipdb.set_trace()
		self.dessert = [food_list[i] for i in items]
		[self.select_item(i) for i in self.dessert]

	def select_vegetables(self):
		if self.yogurt : 
			percent = 0.25
		else:
			percent = 0.18
		calories = percent * self.calories_goal
		food_list = list(filter( lambda x : bool(x.vegetable) , self.marked))
		F,test = knapsack(food_list , calories)
		items = display(F , calories , food_list)
		# import ipdb
		# ipdb.set_trace()
		self.vegetable = [food_list[i] for i in items]
		[self.select_item(i) for i in self.vegetable]

	def select_cereals(self):
		percent = 0.37
		calories = percent * self.calories_goal
		food_list = list(filter( lambda x : bool(x.cereal_grains) , self.marked))
		F,test = knapsack(food_list , calories)
		items = display(F , calories , food_list)
		# import ipdb
		# ipdb.set_trace()
		self.cereals = [food_list[i] for i in items]
		[self.select_item(i) for i in self.cereals]

	def select_pulses(self):
		if self.yogurt : 
			percent = 0.23
		else:
			percent = 0.18
		calories = percent * self.calories_goal
		food_list = list(filter( lambda x : bool(x.pulses) , self.marked))
		F,test = knapsack(food_list , calories)
		items = display(F , calories , food_list)
		# import ipdb
		# ipdb.set_trace()
		self.pulses = [food_list[i] for i in items]
		[self.select_item(i) for i in self.pulses]

	def build(self):
		if self.yogurt:
			self.select_yogurt()
		else:
			self.select_dessert()
		self.select_vegetables()
		self.select_cereals()
		self.select_pulses()
		return self

class M4(Base):
	percent = 0.15

	def __init__(self , calories , goal , exclude = ""):
		self.calories_goal = calories*self.percent
		self.goal = goal
		self.queryset = Food.m4_objects.filter(name__ne = exclude)
		self.marked = list(annotate_food(self.queryset , self.goal))
		self.selected = []
		# heapq.heapify(self.marked)
	
	def select_drink(self):
		calories = 0.15*self.calories_goal
		food_list = list(filter(lambda x : bool(x.drink) , self.marked))
		print(len(food_list) , calories)
		F,test = knapsack(food_list , calories)
		items = display(F , calories , food_list)
		# import ipdb
		# ipdb.set_trace()
		self.drink = [food_list[i] for i in items]
		[self.select_item(i) for i in self.drink]

	def build(self):
		self.select_drink()
		return self

class M5(Base):
	percent = 0.20

	def __init__(self , calories , goal , exclude = ""):
		self.calories_goal = calories*self.percent
		self.goal = goal
		if goal == Goals.WeightLoss : 
			self.queryset = Food.m5loss_objects
		if goal == Goals.WeightGain:
			print("Goal is weight gain")
			self.queryset = Food.m5gain_objects
		self.queryset.filter(name__ne = exclude)
		self.marked = list(annotate_food(self.queryset , self.goal))
		self.selected = []
		# heapq.heapify(self.marked)

	def select_vegetables(self):
		calories = 0.22*self.calories_goal
		food_list = list(filter(lambda x : bool(x.vegetable) , self.marked))
		print(len(food_list) , calories)
		F,test = knapsack(food_list , calories)
		items = display(F , calories , food_list)
		# import ipdb
		# ipdb.set_trace()
		self.vegetables = [food_list[i] for i in items]
		[self.select_item(i) for i in self.vegetables]

	def select_cereals(self):
		calories = 0.39*self.calories_goal
		food_list = list(filter(lambda x : bool(x.cereal_grains) , self.marked))
		F,test = knapsack(food_list , calories)
		items = display(F , calories , food_list)
		self.cereals = [food_list[i] for i in items]
		[self.select_item(i) for i in self.cereals]

	def select_pulses(self):
		calories = 0.39 * self.calories_goal
		food_list = list(filter(lambda x : bool(x.pulses) , self.marked))
		F,test = knapsack(food_list , calories)
		items = display(F , calories , food_list)
		self.pulses = [food_list[i] for i in items]
		[self.select_item(i) for i in self.pulses]

	def build(self):
		self.select_vegetables()
		self.select_cereals()
		self.select_pulses()
		return self
