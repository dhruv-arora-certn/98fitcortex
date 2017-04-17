from .models import Food
from .utils import annotate_food , mark_squared_diff
from .goals import Goals
from knapsack.knapsack_dp import knapsack,display
import heapq , mongoengine , re , random , ipdb , math
from numpy.random import choice


class Base:
	
	def get_max(self , item):
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
		try:
			i = self.get_best_minimum(select_from , calories , name)
		except Exception as e:
			try:
				i = min(select_from , key = lambda x : abs(calories - x.calarie))
			except Exception as e:
				# ipdb.set_trace()
				pass
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
					if item.quantity < 2:
						item.update_quantity(2)
				elif "Tea" not in item.name or "Coffee" not in item.name and not bool(item.yogurt):
					item.update_weight(1.5)	

	def __getitem__(self , key):
		return self.selected[key]

class M1(Base):
	percent = .25

	def __init__(self , calories , goal , exclude=  "" , extra = 0):
		mongoengine.connect(db = "98fit")
		self.calories_goal = calories*self.percent + extra
		self.goal = goal
		self.exclude = exclude
		self.queryset = Food.m1_objects.filter(name__nin = exclude)
		if goal == Goals.WeightLoss : 
			self.queryset = self.queryset.filter(for_loss = 1).all()
		
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
	def rethink(self):
		selected = self.snacks
		if self.calories_remaining > 0:	
			if "Parantha" in selected.name or "Roti" in selected.name or "Dosa" in selected.name or "Cheela" in selected.name:
				steps = math.floor(self.calories_remaining * selected.quantity/(selected.calarie))
				new_quantity = steps + selected.quantity
				selected.update_quantity(new_quantity/selected.quantity)
			else:
				steps = math.floor(self.calories_remaining * selected.weight/(selected.calarie*10))
				new_weight = min(200 , selected.weight + steps * 10)
				selected.update_weight(new_weight/selected.weight)
	
	def build(self):
		self.allocate_restrictions()
		calories = self.calories_remaining
		food_list = list(filter( lambda x : bool(x.snaks) , self.marked))
		self.snacks = self.select_best_minimum(food_list , calories , name = "snacks")
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
		fruit_items = list(Food.m2_objects.filter(fruit= 1).filter(nuts = 1).all())
		try:
			self.fruits = self.select_best_minimum(fruit_items , calories , name = "fruit")
		except Exception as e:
			self.fruits = random.choice(fruit_items)
			self.select_item(self.fruits)

	def select_salad(self):
		self.option = "salad"
		calories = self.calories_goal
		salad_items = list(filter(lambda x : bool(x.salad) , self.marked))
		try:
			self.salad = self.select_best_minimum(salad_items , calories , name = "salad")
		except Exception as e:
			self.salad = random.choice(salad_items)
			self.select_item(self.salad)

	def select_nut(self):
		self.option = "nut"
		calories = self.calories_goal
		nuts_items = list(filter(lambda x : bool(x.nuts) and x.name.startswith("Handful"), self.marked))
		try:
			self.nuts = self.select_best_minimum(nuts_items , calories , name = "nuts")
		except Exception as e:
			self.nuts = random.choice(nuts_items)
			self.select_item(self.nuts)

	def select_snacks(self):
		self.option = "snack"
		calories = self.calories_goal
		snack_items = list(filter(lambda x : bool(x.snaks) , self.marked))
		try:
			self.snack = self.select_best_minimum(snack_items , calories , name = "snack")
		except Exception as e:
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

	def rethink(self):
		steps = round(self.calories_remaining * self.selected[0].weight/(self.selected[0].calarie*10))
		new_weight = self.selected[0].weight + steps * 10
		self.selected[0].update_weight(new_weight/self.selected[0].weight)

	def build(self):
		probability = [
			0.5 , 0.5
		]
		self.choice = choice([
			self.select_fruit , self.select_nut
		], 1 , probability)[0]
		self.choice()
		self.rethink()
		return self


class M3(Base):
	percent = 0.25

	def __init__(self , calories , goal , exclude = "" , extra = 0):
		mongoengine.connect(db = "98fit")
		self.calories_goal = calories*self.percent + extra
		self.extra = extra
		self.goal = goal
		self.queryset = Food.m3_objects.filter(name__nin = exclude)
		self.marked = list(annotate_food(self.queryset , self.goal))
		self.selected = []

	def select_yogurt(self):
		self.isYogurt = True
		calories = 0.15*self.calories_goal
		food_list = Food.m3_objects.filter(yogurt = 1).all()
		self.yogurt = self.select_item(random.choice(food_list) , remove = False)

	def select_dessert(self):
		self.isYogurt = False
		calories = 0.12*self.calories_goal
		food_list = list(filter( lambda x : bool(x.dessert) , self.marked))
		self.dessert = self.select_best_minimum(food_list , calories , name = "dessert")

	def select_vegetables(self , calories = None):
		if self.isYogurt : 
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
		if self.isYogurt : 
			percent = 0.23
		else:
			percent = 0.18
		calories = percent * self.calories_goal
		food_list = list(filter( lambda x : bool(x.pulses) , self.marked))
		try:
			self.pulses = self.select_best_minimum(food_list , calories , "pulses")
		except Exception as e:
			self.pulses = min(food_list , key = lambda x : abs(calories - x.calarie))
			self.select_item(self.pulses)

	def makeGeneric(self):
		self.select_vegetables()
		self.select_cereals()
		self.select_pulses()

	def makeCombinations(self):
		if self.isYogurt:
			calories = (0.25 + 0.37 + 0.23)*self.calories_goal
		else:
			calories = (0.18 + 0.37 + 0.25)*self.calories_goal
		food_list = list(filter(lambda x : x.cuisine == "Combination" , self.marked) )
		self.select_best_minimum(food_list , calories , name = "combination")

			
	def build(self):
		prob_yogurt_dessert = [2/7 , 5/7]
		func1 = choice([
			self.select_yogurt, self.select_dessert
		],
		1 ,  prob_yogurt_dessert)[0]
		func1()
		prob_generic_combination = [2/7,5/7]
		func2 = choice([
			self.makeCombinations, self.makeGeneric
		],
		1 , prob_generic_combination)[0]
		func2()
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
		self.marked = list(filter(lambda x : not x.name.startswith("Handful"),annotate_food(self.queryset , self.goal)))
		self.selected = []
		# heapq.heapify(self.marked)

	def select_drink(self):
		calories = 0.15*self.calories_goal
		food_list = list(filter(lambda x : bool(x.drink) , self.marked))
		try:
			self.drink = self.select_best_minimum(food_list , calories , "drink")
		except Exception as e:
			self.drink = random.choice(food_list)
			self.select_item(self.drink)

	def select_fruit(self):
		self.option = "fruits"
		calories = self.calories_goal
		fruit_items = list(filter(lambda x : bool(x.fruit) , self.marked))
		self.fruits = self.select_best_minimum(fruit_items , calories , "fruit")
		self.fruits.update_quantity(2)

	def select_salad(self):
		self.option = "salad"
		calories = self.calories_goal
		salad_items = list(filter(lambda x : bool(x.salad) and not x.name.startswith("Handful"), self.marked))
		self.salad = self.select_best_minimum(salad_items , calories , "salad")
		self.salad.update_weight(1.5)

	def select_nut(self):
		self.option = "nuts"
		calories = self.calories_goal
		nuts_items = list(filter(lambda x : bool(x.nuts) and x.calarie < self.calories_remaining, self.marked))
		self.nuts = self.select_best_minimum(nuts_items , calories , "nuts")
		self.nuts.update_quantity(2)

	def select_snacks(self):
		self.option = "snacks"
		calories = self.calories_goal
		snack_items = list(filter(lambda x : bool(x.snaks) and x.calarie < self.calories_remaining, self.marked))
		self.snacks = self.select_best_minimum(snack_items , calories , "snacks")

	def rethink(self):
		selected = getattr(self , self.option)
		if self.option == "fruits" or self.option == "nuts":
			steps = round(self.calories_remaining * selected.quantity/(selected.calarie))
			new_quantity = steps + selected.quantity
			selected.update_quantity(new_quantity/selected.quantity)
		else:
			steps = round(self.calories_remaining * selected.weight/(selected.calarie*10))
			new_weight = min(250,selected.weight + steps * 10)
			selected.update_weight(new_weight/selected.weight)

	def build(self):
		self.select_drink()
		probability = [0.25 , 0.25 , 0.25 , 0.25]
		func = choice([
			self.select_fruit , self.select_nut , self.select_snacks , self.select_salad
		], 1 , probability)[0]
		func()
		self.rethink()
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
