from .models import Food
from .utils import annotate_food , mark_squared_diff
from .goals import Goals
from knapsack.knapsack_dp import knapsack,display
import heapq , mongoengine , re

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

	@property
	def protein_ideal(self):
		return (self.goal.protein * self.calories_goal) / 4

	@property
	def carbs_ideal(self):
		return (self.goal.carbs * self.calories_goal) / 4

	@property
	def fat_ideal(self):
		return (self.goal.fat * self.calories_goal ) / 9

	@property
	def protein(self):
		return sum([i.protein for i in self.selected])

	@property
	def fat(self):
		return sum([i.fat for i in self.selected])

	@property
	def carbs(self):
		return sum([i.carbohydrates for i in self.selected])

	def __getitem__(self , key):
		return self.selected[key]

class M1(Base):
	percent = .25

	def __init__(self , calories , goal , exclude=  "" , extra = 0):
		mongoengine.connect(db = "98fit")
		self.calories_goal = calories*self.percent + extra
		self.goal = goal
		self.queryset = Food.m1_objects.filter(name__nin = exclude)
		if goal == Goals.WeightLoss : 
			self.queryset.filter(for_loss = 1).all()
		
		self.marked = list(annotate_food(self.queryset , self.goal))
		self.selected = []
		# heapq.heapify(self.marked)

	def allocate_restrictions(self):
		self.select_item(self.drink)
		self.remove_drinks()
		self.select_item(mark_squared_diff(Food.m1_objects.filter(name = "Boiled Egg White").first() , self.goal.get_attributes()))
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

	def filter_parantha(self):
		paranthas = [e for e in self.selected if re.search("Parantha" , e.name)]
		if paranthas:
			[self.selected.remove(p) for p in paranthas]
			calories = sum([e.calorie for e in paranthas])
			parantha = min(paranthas)
			calories_req = calories - parantha.calorie
			amount = round(calories_req/parantha.calorie)
			parantha.quantity = amount
			self.selected.append(parantha)
		return self

	def build(self):
		print("Starting 1")
		self.allocate_restrictions()
		calories = self.calories_remaining
		food_list = list(filter( lambda x : bool(x.snaks) , self.marked))
		F,test = knapsack(food_list , calories)
		items = display(F , calories , food_list)
		# import ipdb
		# ipdb.set_trace()
		self.snacks = [food_list[i] for i in items]
		[self.select_item(i) for i in self.snacks]
		self.filter_parantha()
		return self


class M2(Base):
	percent = 0.15

	def __init__(self , calories , goal , exclude , extra = 0):
		mongoengine.connect(db = "98fit")
		self.calories_goal = calories*self.percent + extra
		self.goal = goal
		self.queryset = Food.m2_objects.filter(salad = 0).filter(name__nin = exclude)
		self.marked = list(annotate_food(self.queryset , self.goal))
		self.selected = []

	def select_fruit(self):
		calories = self.calories_goal
		fruit_items = self.marked
		F,test = knapsack(fruit_items , self.calories_goal)
		items = display(F , self.calories_goal , fruit_items)
		self.fruits = min([fruit_items[i] for i in items])
		self.fruits.update((calories/self.fruits.calarie))
		self.select_item(self.fruits)

	def build(self):
		self.select_fruit()
		return self


class M3(Base):
	percent = 0.25

	def __init__(self , calories , goal , exclude = "" , yogurt = True , extra = 0):
		mongoengine.connect(db = "98fit")
		self.calories_goal = calories*self.percent + extra
		self.goal = goal
		self.queryset = Food.m3_objects.filter(salad = 0).filter(name__nin = exclude)
		self.yogurt = yogurt
		self.marked = list(annotate_food(self.queryset , self.goal))
		self.selected = []

	def select_yogurt(self):
		calories = 0.15*self.calories_goal
		food_list = list(filter( lambda x : bool(x.yogurt) , self.marked))
		F,test = knapsack(food_list , calories)
		items = display(F , calories , food_list)
		self.yogurt = min([food_list[i] for i in items])
		self.select_item(self.yogurt)

	def select_dessert(self):
		calories = 0.12*self.calories_goal
		food_list = list(filter( lambda x : bool(x.dessert) , self.marked))
		F,test = knapsack(food_list , calories)
		items = display(F , calories , food_list)
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
		self.vegetables = min([food_list[i] for i in items])
		self.vegetables.update(calories/self.vegetables.calarie)
		self.select_item(self.vegetables)

	def select_cereals(self):
		percent = 0.37
		calories = percent * self.calories_goal
		food_list = list(filter( lambda x : bool(x.cereal_grains) , self.marked))
		F,test = knapsack(food_list , calories)
		items = display(F , calories , food_list)
		# import ipdb
		# ipdb.set_trace()
		self.cereals = min([food_list[i] for i in items])
		self.cereals.update(calories/self.cereals.calarie)
		self.select_item(self.cereals)

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
		self.pulses = min([food_list[i] for i in items])
		self.pulses.update(calories/self.pulses.calarie)
		self.select_item(self.pulses)

	def build(self):
		print("Starting 3")
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

	def __init__(self , calories , goal , exclude = "" , extra = 0):
		mongoengine.connect(db = "98fit")
		self.calories_goal = calories*self.percent + extra
		self.goal = goal
		self.queryset = Food.m4_objects.filter(name__nin = exclude)
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
		self.drink = min([food_list[i] for i in items])
		self.drink.update(calories/self.drink.calarie)
		self.select_item(self.drink)

	def select_snack(self):
		calories = 0.85*self.calories_goal
		food_list = list(filter(lambda x : bool(x.snaks) , self.marked))
		print(len(food_list) , calories)
		F,test = knapsack(food_list , calories)
		items = display(F , calories , food_list)
		# import ipdb
		# ipdb.set_trace()
		self.snacks = min([food_list[i] for i in items])
		self.snacks.update(calories/self.snacks.calarie)
		self.select_item(self.snacks)		

	def build(self):
		self.select_drink()
		self.select_snack()
		return self

class M5(Base):
	percent = 0.20

	def __init__(self , calories , goal , exclude = "" , extra = 0):
		mongoengine.connect(db = "98fit")
		self.calories_goal = calories*self.percent + extra
		self.goal = goal
		if goal == Goals.WeightLoss : 
			self.queryset = Food.m5loss_objects
		if goal == Goals.WeightGain or goal == Goals.MuscleGain:
			self.queryset = Food.m5gain_objects
		if goal == Goals.MaintainWeight:
			self.queryset = Food.m5stable_objects

		self.queryset.filter(name__nin = exclude)
		self.marked = list(annotate_food(self.queryset , self.goal))
		self.selected = []
		# heapq.heapify(self.marked)

	def select_vegetables(self):
		calories = 0.22*self.calories_goal
		self.vegetable_calories = calories
		food_list = list(filter(lambda x : bool(x.vegetable) , self.marked))
		print(len(food_list) , calories)
		F,test = knapsack(food_list , calories)
		items = display(F , calories , food_list)
		# import ipdb
		# ipdb.set_trace()
		self.vegetables = min([food_list[i] for i in items])
		self.vegetables.update(calories/self.vegetables.calarie)
		self.select_item(self.vegetables)

	def select_cereals(self):
		calories = 0.39*self.calories_goal
		food_list = list(filter(lambda x : bool(x.cereal_grains) , self.marked))
		F,test = knapsack(food_list , calories)
		items = display(F , calories , food_list)
		self.cereals = min([food_list[i] for i in items])
		self.cereals.update(calories/self.cereals.calarie)
		self.select_item(self.cereals)

	def select_pulses(self):
		calories = 0.39 * self.calories_goal
		food_list = list(filter(lambda x : bool(x.pulses) , self.marked))
		F,test = knapsack(food_list , calories)
		items = display(F , calories , food_list)
		self.pulses = min([food_list[i] for i in items])
		self.pulses.update(calories/self.pulses.calarie)
		self.select_item(self.pulses)

	def build(self):
		self.select_vegetables()
		self.select_cereals()
		self.select_pulses()
		return self
