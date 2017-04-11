from .models import Food
from .utils import annotate_food , mark_squared_diff
from .goals import Goals
from knapsack.knapsack_dp import knapsack,display
import heapq , mongoengine , re , random , ipdb
from numpy.random import choice


class Base:
	
	def get_max(self , item):
		print("Calling get max")
		goal = self.goal
		return item.goal_nutrition(goal)

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

	@property
	def calories_remaining(self):
		return self.calories_goal - self.calories

	def random(self):
		return random.sample(self.for_random , min(2,len(self.selected)))

	@property
	def for_random(self):
		return self.selected

	def get_best(self, select_from , calories , name):
		F,test = knapsack(select_from, calories)
		a = [select_from[i] for i in display(F , calories , select_from)]
		setattr(self , name + "_options" , a)
		return a
	
	def get_best_minimum(self , select_from , calories , name):
		return min(self.get_best(select_from , calories , name))

	def select_best_minimum(self , select_from , calories , name):
		i = self.get_best_minimum(select_from , calories , name)
		self.select_item(i)
		return i

	def select_item(self , item , remove = True):
		self.selected.append(item)
		if remove:
			self.marked.remove(item)
		return self

	def unselect_item(self , item , append = True):
		self.selected.remove(item)
		if append:
			self.selected.append(item)
		return self

	def select_items(self , *items):
		[self.select_item(e) for e in items]
		return self

	def rethink(self):
		for item in self.selected:
			if self.calories < self.calories_goal:
				if "Parantha" in item.name or "Roti" in item.name or "Cheela" in item.name:
					print("Updating Quantity" , item)
					if item.quantity < 2:
						item.update_quantity(2)
				elif "Tea" not in item.name or "Coffee" not in item.name:
					print("Updating Weight" , item)
					item.update_weight(1.5)	

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
		self.egg = mark_squared_diff(Food.m1_objects.filter(name = "Boiled Egg White").first() , self.goal.get_attributes())
		self.select_item(self.egg , remove = False)

	def pop_snack(self):
		self.snack_list = list(filter(lambda x : x.snaks , self.marked ))
		heapq.heapify(self.snack_list)
		return heapq.heappop(self.snack_list)	

	@property
	def drink(self):
		self.drink_list = list(filter( lambda x : x.drink & x.dairy , self.marked))
		return min(self.drink_list , key = lambda x : (self.calories_goal * 0.15 - x.calorie)**2)

	def remove_drinks(self):
		self.marked = list(set(self.marked) - set(self.drink_list))
		return self

	def rethink(self):
		for item in self.selected:
			if self.calories < self.calories_goal and item != self.egg:
				if "Parantha" in item.name or "Roti" in item.name or "Dosa" in item.name or "Cheela" in item.name:
					item.update_quantity(2)
				else:
					item.update_weight(1.5)
	
	def build(self):
		print("Starting 1")
		self.allocate_restrictions()
		calories = self.calories_remaining
		food_list = list(filter( lambda x : bool(x.snaks) , self.marked))
		try:
			self.snacks = sorted(self.get_best(food_list , calories , name = "snacks"))
		except IndexError as e:
			self.snacks = [random.choice(food_list)]
		if len(self.snacks) >= 2:
			self.select_items(*self.snacks[:1])
			# self.select_item(self.egg)
			print(len(self.snacks))
		else:
			self.select_items(*self.snacks)
		if self.protein_ideal - self.protein > 8:
			self.select_item(self.egg , remove = False)
		self.rethink()
		return self


class M2(Base):
	percent = 0.15

	def __init__(self , calories , goal , exclude , extra = 0):
		mongoengine.connect(db = "98fit")
		self.calories_goal = calories*self.percent + extra
		self.goal = goal
		self.queryset = Food.m2_objects.filter(name__nin = exclude)
		self.marked = list(annotate_food(self.queryset , self.goal))
		self.selected = []

	def select_fruit(self):
		self.option = "fruit"
		calories = self.calories_goal
		fruit_items = list(filter(lambda x : bool(x.fruit) , self.marked))
		try:
			self.fruits = self.select_best_minimum(fruit_items , calories , name = "fruit")
		except IndexError as e:
			self.fruits = random.choice(fruit_items)
			self.select_item(self.fruits)

	def select_salad(self):
		self.option = "salad"
		calories = self.calories_goal
		salad_items = list(filter(lambda x : bool(x.salad) , self.marked))
		try:
			self.salad = self.select_best_minimum(salad_items , calories , name = "salad")
		except IndexError as e:
			self.salad = random.choice(salad_items)
			self.select_item(self.salad)

	def select_nut(self):
		self.option = "nut"
		calories = self.calories_goal
		print("Nut calories" , calories)
		nuts_items = list(filter(lambda x : bool(x.nuts) , self.marked))
		try:
			self.nuts = self.select_best_minimum(nuts_items , calories , name = "nut")
		except IndexError as e:
			self.nuts = random.choice(nuts_items)
			self.select_item(self.nuts)

	def select_snacks(self):
		self.option = "snack"
		calories = self.calories_goal
		snack_items = list(filter(lambda x : bool(x.snaks) , self.marked))
		try:
			self.snack = self.select_best_minimum(snack_items , calories , name = "snack")
		except IndexError as e:
			self.snack = random.choice(snack_items)
			self.select_item(self.snack)

	def check(self):
		choices = ["snack" , "nut" , "salad" , "fruit"]
		f = Food.m2_objects
		choices.remove(self.option)
		choice = random.choice(choices)
		if choice == "snack":
			f = f.filter(snaks = 1)
		if choice == "nut":
			f = f.filter(nuts = 1)
		if choice == "salad":
			f = f.filter(salad = 1)
		if choice == "fruit":
			f = f.filter( fruit = 1)
		f = f.filter(calarie__lt = self.calories_remaining)
		if f:
			val = min(f)
			setattr(self, choice , val)
			self.select_item(val , remove = False)		
	def build(self):
		probability = [
			0.4 , 0.2 ,0.2, 0.2
		]
		self.choice = choice([
			self.select_fruit , self.select_nut , self.select_snacks , self.select_salad
		], 1 , probability)[0]
		self.choice()
		self.check()
		return self


class M3(Base):
	percent = 0.25

	def __init__(self , calories , goal , exclude = "" , yogurt = True , extra = 0):
		mongoengine.connect(db = "98fit")
		self.calories_goal = calories*self.percent + extra
		self.extra = extra
		self.goal = goal
		self.queryset = Food.m3_objects.filter(name__nin = exclude)
		self.yogurt = yogurt
		self.marked = list(annotate_food(self.queryset , self.goal))
		self.selected = []

	def select_yogurt(self):
		calories = 0.15*self.calories_goal
		food_list = Food.m3_objects.filter(yogurt = 1).all()
		print("Yogurt " , food_list)
		self.yogurt = self.select_item(random.choice(food_list) , remove = False)

	def select_dessert(self):
		calories = 0.12*self.calories_goal
		food_list = list(filter( lambda x : bool(x.dessert) , self.marked))
		self.dessert = self.select_best_minimum(food_list , calories , name = "dessert")

	def select_vegetables(self , calories = None):
		if self.yogurt : 
			percent = 0.25
		else:
			percent = 0.18
		
		if not calories:
			calories = percent * self.calories_goal
		
		food_list = list(filter( lambda x : bool(x.vegetable) , self.marked))
		self.vegetables = self.select_best_minimum(food_list , calories , "vegetables")

	def select_cereals(self , percent = 0.37):		
		calories = percent * self.calories_goal
		food_list = list(filter( lambda x : bool(x.cereal_grains) and not bool(x.dessert) , self.marked))
		self.cereals = self.select_best_minimum(food_list , calories , "cereals")
		if "Parantha" in self.cereals.name or "Roti" in self.cereals.name:
			if self.cereals.quantity < 2:
				self.cereals.update_quantity(2)

	def select_pulses(self):
		if self.yogurt : 
			percent = 0.23
		else:
			percent = 0.18
		calories = percent * self.calories_goal
		food_list = list(filter( lambda x : bool(x.pulses) , self.marked))
		self.pulses = self.select_best_minimum(food_list , calories , "pulses")

	def build(self):
		print("Starting 3")
		if self.yogurt:
			self.select_yogurt()
		else:
			self.select_dessert()
		self.select_vegetables()
		self.select_cereals()
		self.select_pulses()
		self.rethink()
		return self

	@property
	def for_random(self):
		return list(filter( lambda x : not bool(x.dessert) , self.selected))

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
		try:
			self.drink = self.select_best_minimum(food_list , calories , "drink")
		except IndexError as e:
			self.drink = random.choice(food_list)
			self.select_item(self.drink)

	def select_fruit(self):
		calories = self.calories_goal
		fruit_items = list(filter(lambda x : bool(x.fruit) , self.marked))
		try:
			self.fruits = self.select_best_minimum(fruit_items , calories , "fruit")
		except IndexError as e:
			self.fruits = random.choice(food_list)
			self.select_item(self.fruits)
		self.fruits.update_quantity(2)

	def select_salad(self):
		calories = self.calories_goal
		salad_items = list(filter(lambda x : bool(x.salad) , self.marked))
		try:
			self.salad = self.select_best_minimum(salad_items , calories , "salad")
		except IndexError as e:
			self.salad = random.choice(salad_items)
			self.select_item(self.salad)
		self.salad.update_weight(1.5)

	def select_nut(self):
		calories = self.calories_goal
		print("Nut calaories m4 ",calories)
		nuts_items = list(filter(lambda x : bool(x.nuts) , self.marked))
		self.nuts = self.select_best_minimum(nuts_items , calories , "nut")
		self.nuts.update_quantity(2)

	def select_snacks(self):
		calories = self.calories_goal
		snack_items = list(filter(lambda x : bool(x.snaks) , self.marked))
		try:
			self.snack = self.select_best_minimum(snack_items , calories , "snacks")
		except IndexError as e:
			self.snack = random.choice(snack_items)
			self.select_item(self.snack)

	def build(self):
		self.select_drink()
		probability = [0.25 , 0.25 , 0.25 , 0.25]
		func = choice([
			self.select_fruit , self.select_nut , self.select_snacks , self.select_salad
		], 1 , probability)[0]
		func()
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
		self.queryset = self.queryset.filter(name__nin = exclude).filter(name__nin = ["Beetroot Parantha"])
		self.marked = list(annotate_food(self.queryset , self.goal))
		self.selected = []
		# heapq.heapify(self.marked)

	def select_vegetables(self):
		calories = 0.22*self.calories_goal
		self.vegetable_calories = calories
		food_list = list(filter(lambda x : bool(x.vegetable) , self.marked))
		self.vegetables = self.select_best_minimum(food_list , calories , "vegetables")

	def select_cereals(self):
		calories = 0.39*self.calories_goal
		food_list = list(filter(lambda x : bool(x.cereal_grains) , self.marked))
		self.cereals = self.select_best_minimum(food_list , calories , "cereals")

	def select_pulses(self):
		calories = 0.39 * self.calories_goal
		food_list = list(filter(lambda x : bool(x.pulses) , self.marked))
		self.pulses = self.select_best_minimum(food_list , calories , "pulses")

	def build(self):
		self.select_cereals()
		self.select_pulses()
		self.select_vegetables()
		self.rethink()
		return self
