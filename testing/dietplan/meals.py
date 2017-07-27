from epilogue.models import Food , GeneratedDietPlan
from .utils import annotate_food , mark_squared_diff
from .goals import Goals
from .medical_conditions import Osteoporosis , Anemia
from knapsack.knapsack_dp import knapsack,display
import heapq ,  re , random , ipdb , math
from django.db.models import Q
from numpy.random import choice
from epilogue.manipulation.manipulator import Manipulator
from dietplan.categorizer.categorizers import *

class Base:
	fieldMapper = {
		Goals.WeightLoss : "squared_diff_weight_loss",
		Goals.MaintainWeight : "squared_diff_weight_maintain",
		Goals.WeightGain : "squared_diff_weight_gain",
		Goals.MuscleGain : "squared_diff_muscle_gain"
	}
	def get_max(self , item):
		goal = self.goal
		return item.goal_nutrition(goal)

	def get_steps(self , item):
		difference = self.calories_goal - self.calories
		unit = item.calarie/(5*item.weight)
		steps = round(difference/unit)
		return steps
	
	@property
	def calories(self):
		return sum([i.calorie for i in self.selected.values()])

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
		return sum([i.protein for i in self.selected.values()])

	@property
	def fat(self):
		return sum([i.fat for i in self.selected.values()])

	@property
	def carbs(self):
		return sum([i.carbohydrates for i in self.selected.values()])

	@property
	def calories_remaining(self):
		return self.calories_goal - self.calories

	def random(self):
		return random.sample(self.for_random , min(2,len(self.selected.values())))

	@property
	def for_random(self):
		return self.selected

	def get_best(self, select_from , calories , name):
		F,test = knapsack(select_from, calories , self.fieldMapper.get(self.goal) )
		a = [select_from[i] for i in display(F , calories , select_from)]
		setattr(self , name + "_options" , a)
		return a
	
	def get_best_minimum(self , select_from , calories , name):
		return min(self.get_best(select_from , calories , name) , key = lambda x : getattr(x , self.fieldMapper.get(self.goal)))

	def select_best_minimum(self , select_from , calories , name):
		try:
			i = self.get_best_minimum(select_from , calories , name)
		except Exception as e:
			print("Some MF _____" , e)
			i = min(select_from , key = lambda x : abs(calories - x.calorie) )
		else:
			i = min(select_from , key = lambda x : abs(calories - x.calorie))
		finally:
			self.select_item(i , name)
			return i

	def select_item(self , item , key , remove = True):
		if item is None:
			return
		self.selected.update({
			key : item
		})
		if remove:
			self.marked.exclude(id = item.id)
		return item

	def unselect_item(self , item , append = True):
		self.selected.remove(item)
		if append:
			self.selected.append(item)
		return self

	def select_items(self , *items):
		[self.select_item(e) for e in items]
		return self

	def rethink(self):
		for item in self.selected.values():
			if self.calories < self.calories_goal:
				if "Parantha" in item.name or "Roti" in item.name or "Cheela" in item.name:
					if item.quantity < 2:
						item.update_quantity(2)
				elif "Tea" not in item.name or "Coffee" not in item.name and not bool(item.yogurt):
					item.update_weight(1.5)
	def build(self):
		if self.disease is not None:
			pass

	def __getitem__(self , key):
		return self.selected[key]

class M1(Base):
	percent = .25

	def __init__(self , calories , goal , exclude=  "" , extra = 0 , disease = None , exclusion_conditions = Q() , selected = None):
		self.calories_goal = calories*self.percent + extra
		self.goal = goal
		self.exclude = exclude
		self.disease = disease
		self.exclusion_conditions = exclusion_conditions
		self.queryset = Food.m1_objects.exclude(name__in = exclude)
		self.queryset = self.queryset.filter(self.exclusion_conditions)

		if goal == Goals.WeightLoss : 
			self.queryset = self.queryset.filter(for_loss = '1').all()
		
		if self.disease and hasattr(self.disease , "queryset_filter"): 
			self.queryset = self.queryset.filter(self.disease.queryset_filter)		
		
		self.marked = self.queryset
		self.selected = selected

		self.buildMapper = {
			'snack' : self.select_snack,
			'drink' : self.select_drink
		}
		backwardMapper ={
			'snaks' : self.select_snack,
			'pulses' : self.select_snack
		}
		self.buildMapper.update(backwardMapper)

	def allocate_restrictions(self):
		self.drink = self.select_item(self.get_drink , "drink")
		self.remove_drinks()

		if  ('egg' , 0) not in self.exclusion_conditions.children and not hasattr(self,"egg"):
			self.egg = Food.m1_objects.filter(name = "Boiled Egg White").first()
			self.select_item(self.egg , "egg" ,remove = False)

	def pop_snack(self):
		# self.snack_list = list(filter(lambda x : x.snaks , self.marked ))
		self.snack_list = self.marked.filter(snaks = '1').filter(dairy = 0)
		heapq.heapify(self.snack_list)
		return heapq.heappop(self.snack_list)	
	
	@property
	def get_drink(self):
		self.drink_list = self.marked.filter(drink = '1').filter(size = "Teacup")
		if ('dairy',0) not in self.exclusion_conditions.children:
			self.drink_list = self.drink_list.filter(dairy = '1')
		if not self.drink_list.count():
			return
		m = Manipulator(items = self.drink_list , categorizers = [DrinkCategoriser])
		self.drink_list = m.categorize().get_final_list()
		return min(self.drink_list , key = lambda x : abs(self.calories_goal * 0.15 - x.calorie))

	def select_drink(self):
		self.select_item(self.get_drink , "drink")

	def remove_drinks(self):
		# self.marked = list(set(self.marked) - set(self.drink_list))
		self.marked = self.marked.exclude(name__in = [e.name for e in self.drink_list])
		return self

	def rethink(self):
		print("Running M1 rethink")
		selected = self.snack
		if self.calories_remaining > 0 and isinstance(selected, Food):	
			if "Roti" in selected.name or "Dosa" in selected.name or "Cheela" in selected.name or "Bun" in selected.name:
				steps = math.floor(self.calories_remaining * selected.quantity/(selected.calarie))
				new_quantity = steps + selected.quantity
				selected.update_quantity(new_quantity/selected.quantity)
			else:
				print("Updatin " , selected , selected.weight)
				steps = math.floor(self.calories_remaining * selected.weight/(selected.calarie*10))
				new_weight =  selected.weight + steps * 10
				selected.update_weight(new_weight/selected.weight)
				print("New weight" , selected.weight)
	
	def select_snack(self):
		calories = self.calories_goal
		if ("dairy",0) not in self.exclusion_conditions:
			calories *= 0.85
		food_list = self.marked.filter(snaks = '1').filter(dairy = 0)
		if not ("egg",0) in self.exclusion_conditions.children:
			food_list = food_list.exclude(egg = 1	)
			calories -= 36
		m = Manipulator(items = food_list , categorizers = [ParanthaCategoriser])
		food_list = m.categorize().get_final_list()
		self.snack = self.select_best_minimum(food_list , calories , name = "snack")
		 
	def build(self):
		self.allocate_restrictions()
		self.select_snack()
		if self.protein_ideal - self.protein > 8 and hasattr(self , "egg"):
			self.egg.update_quantity(1.5)
		self.rethink()
		return self


class M2(Base):
	percent = 0.15

	def __init__(self , calories , goal , exclude , extra = 0 , disease = None , exclusion_conditions = None , selected = None):
		self.calories_goal = calories*self.percent + extra
		self.goal = goal
		self.exclude = exclude
		self.queryset = self.getDefaultQueryset().exclude(name__in = exclude)

		if self.goal == Goals.WeightLoss:
			self.queryset = self.queryset.filter(for_loss = 1)

		self.marked = self.queryset
		self.selected = selected
		self.exclusion_conditions = exclusion_conditions

		if self.exclusion_conditions : 
			self.queryset = self.queryset.filter(self.exclusion_conditions)

		self.buildMapper = {
			'nut' : self.select_nut,
			'salad' : self.select_salad,
			'fruit' : self.select_fruit,
			'snack' : self.select_snacks
		}
		backwardMapper = {
			'fruits' : self.select_fruit,
			'nuts' : self.select_nut,
			'pulses' : self.select_snacks,
			'snaks' : self.select_snacks
		}
		self.buildMapper.update(backwardMapper)

	def getDefaultQueryset(self):
		return Food.m2_objects

	def select_fruit(self):
		self.option = "fruit"
		calories = self.calories_goal
		fruit_items = Food.m2_objects.filter(fruit= 1)
		try:
			self.fruit = self.select_best_minimum(fruit_items , calories , name = "fruit")
		except Exception as e:
			print("From M2 Fruit " , e)
			self.fruit = random.choice(fruit_items)
			self.select_item(self.fruits , "fruits")

	def select_salad(self):
		self.option = "salad"
		calories = self.calories_goal
		salad_items = self.marked.filter(salad = 1)
		try:
			self.salad = self.select_best_minimum(salad_items , calories , name = "salad")
		except Exception as e:
			self.salad = random.choice(salad_items)
			self.select_item(self.salad , "salad")

	def select_nut(self):
		self.option = "nut"
		calories = self.calories_goal
		nuts_items = self.marked.filter(Q(name__startswith = "Handful")).all()
		if not nuts_items.count():
			nuts_items = self.getDefaultQueryset().filter(Q(name__startswith = "Handful"))
		try:
			self.nuts = self.select_best_minimum(nuts_items , calories , name = "nuts")
		except Exception as e:
			# ipdb.set_trace()
			self.nuts = random.choice(nuts_items)
			self.select_item(self.nuts , "nuts")

	def select_snacks(self):
		self.option = "snack"
		calories = self.calories_goal
		snack_items = self.marked.filter(snaks = 1)
		try:
			self.snack = self.select_best_minimum(snack_items , calories , name = "snack")
		except Exception as e:
			self.snack = random.choice(snack_items)
			self.select_item(self.snack , "snack")

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
		for e in self.selected.values():
			steps = round(self.calories_remaining * e.weight/(e.calarie*10))
			new_weight = e.weight + steps * 10
			e.update_weight(new_weight/e.weight)

	def get_probability(self):
		print("Calling get Probability")
		if ('nuts' , 0) in self.exclusion_conditions.children:
			print("No nuts")
			return [1,0]
		return [0.5,0.5]

	def build(self):
		if ('nuts' , 0) in self.exclusion_conditions.children:
			self.select_fruit()
		else:
			self.choice = choice([self.select_fruit , self.select_nut],
				size = 1,
				p = [0.5 , 0.5]
			)[0]
			self.choice()
		self.rethink()
		return self


class M3(Base):
	percent = 0.25

	def __init__(self , calories , goal , exclude = "" , extra = 0 , disease = None , exclusion_conditions = None , make_combination = False , make_dessert = False ,  exclude2 = None , selected = None):
		self.calories_goal = calories*self.percent + extra
		self.extra = extra
		self.goal = goal
		self.disease = disease
		self.exclude2 = exclude2
		self.selected = selected
		self.queryset = self.getQuerysetFromGoal().exclude(name__in = exclude)

		if self.goal == Goals.WeightLoss:
			self.queryset = self.queryset.filter(for_loss = 1)

		if self.disease:
			self.queryset = self.queryset.filter(self.disease.queryset_filter)

		self.exclusion_conditions = exclusion_conditions
		self.queryset = self.queryset.filter(exclusion_conditions)
		self.marked = self.queryset
		self.make_combination = make_combination
		self.make_dessert = make_dessert
		self.isYogurt = False

		self.buildMapper = {
			'yogurt' : self.select_yogurt,
			'dessert' : self.select_dessert,
			'vegetable' : self.select_vegetables,
			'pulse' : self.select_pulses,
			'cereal' : self.select_cereals,
			'combination' : self.makeCombinations
		}
		backwardMapper = {
			'cereals' : self.select_cereals,
			'grains_cereals' : self.select_cereals,
			'pulses' : self.select_pulses,
		}
		self.buildMapper.update(backwardMapper)

	def getQuerysetFromGoal(self):
		f = Food.m3_objects.filter(for_loss = 1)
		return f

	def select_yogurt(self):
		self.isYogurt = True
		calories = 0.15*self.calories_goal
		food_list = self.marked.filter(yogurt = 1)
		food_list = food_list.filter(self.exclusion_conditions)
		m = Manipulator(items = food_list , categorizers = [YogurtCategoriser])
		food_list = m.categorize().get_final_list()
		# ipdb.set_trace()
		self.yogurts = self.select_best_minimum(food_list , calories , name="yogurt")
		
		if isinstance(self.yogurts , Food):
			steps = round( (calories - self.yogurts.calorie) * self.yogurts.weight/(self.yogurts.calorie*10))
			new_weight = min(250,self.yogurts.weight + steps * 10)
			self.yogurts.update_weight(new_weight/self.yogurts.weight)

	def select_dessert(self):
		self.isYogurt = False
		calories = 0.12*self.calories_goal
		food_list = self.marked.filter(dessert = 1)
		self.dessert = self.select_best_minimum(food_list , calories , name = "dessert")

	def select_vegetables(self , calories = None):
		if self.isYogurt : 
			percent = 0.25
		else:
			percent = 0.18
		
		if not calories:
			calories = percent * self.calories_goal
		food_list = self.marked.filter(vegetable = 1).filter(grains_cereals = 0).filter(cuisine = "Generic")
		if self.disease and hasattr(self.disease , "vegetable_filter"):
			food_list = food_list.filter(self.disease.vegetable_filter)
		m = Manipulator(items = food_list , categorizers = [VegetablePulseCategoriser])
		food_list = m.categorize().get_final_list()
		self.vegetable = self.select_best_minimum(food_list , calories , "vegetable")
		
		if isinstance(self.vegetable , Food):
			steps = round((calories - self.vegetable.calarie ) * self.vegetable.weight/(self.vegetable.calarie*10))
			new_weight = min(250,self.vegetable.weight + steps * 10)
			self.vegetable.update_weight(new_weight/self.vegetable.weight)


	def select_cereals(self , percent = 0.37):		
		calories = percent * self.calories_goal
		
		if self.exclude2:
			food_list = self.getQuerysetFromGoal().exclude(name__in = self.exclude2).filter(grains_cereals = 1)
			food_list = food_list.filter(self.exclusion_conditions)
		else:
			food_list = self.marked.filter(grains_cereals = 1)
			food_list = food_list.filter(self.exclusion_conditions)
		
		food_list = food_list.filter(cuisine = "Generic")
		# ipdb.set_trace()
		m = Manipulator(items = food_list , categorizers = [GrainsCerealsCategoriser])
		food_list = m.categorize().get_final_list()
		self.cereal = self.select_best_minimum(food_list , calories , "cereals")
		
	def select_pulses(self , calories = None , non_veg = False):
		
		if self.isYogurt : 
			percent = 0.23
		else:
			percent = 0.18
		
		if not calories:
			calories = percent * self.calories_goal
		
		if 	non_veg:
			food_list = self.marked.filter( Q(non_veg_gravy_items = 1) | Q(pulses = 1)  & Q(vegetable = 1) & Q(cuisine = "Generic") & Q(grains_cereals = 0))
		else:
			food_list = self.marked.filter(pulses = 1).filter(grains_cereals = 0).filter(cuisine = "Generic")
		
		m = Manipulator(items = food_list , categorizers = [VegetablePulseCategoriser])
		food_list = m.categorize().get_final_list()
		try:
			self.pulses = self.select_best_minimum(food_list , calories , "pulse")
		except Exception as e:
			self.pulses = min(food_list , key = lambda x : abs(calories - x.calarie))
			self.select_item(self.pulses , "pulse")

	def makeGeneric(self):
		self.select_cereals()
		
		#Already Implemented
		if self.cereal.vegetables == 1 and self.cereal.pulse == 0:
			self.select_pulses(calories = self.calories_remaining)
		
		elif self.cereal.vegetables == 0 and self.cereal.pulse == 1:
			self.select_vegetables(calories = self.calories_remaining)
		
		#Already Implemented
		elif self.cereal.vegetables == 1 and self.cereal.pulse == 1:
			self.select_pulses(calories = self.calories_remaining)
		
		elif self.cereal.non_veg == 1:
			self.select_pulses(non_veg = True)

		if self.cereal.vegetables == 0 and self.cereal.pulse == 0:
			self.select_pulses()
			self.select_vegetables()	
		return self

	def makeCombinations(self):
		calories = self.calories_remaining
		if self.make_dessert:
			calories *= 0.88
		else:
			calories *= 0.85
		food_list = self.marked.filter(cuisine = "Combination")
		self.combination = self.select_best_minimum(food_list , calories , name = "combination")
		steps = round( (calories-self.combination.calarie) * self.combination.weight/(self.combination.calarie*10))
		new_weight = min(350,self.combination.weight + steps * 10)
		self.combination.update_weight(new_weight/self.combination.weight)

	def rethink(self):
		if self.calories < self.calories_goal:
			if hasattr(self,"combination"):
				selected = self.combination
			elif hasattr(self , "pulses" ):
				selected = self.pulses
			elif hasattr(self , "vegetables"):
				selected = self.vegetables
			try:
				new_weight = min(200,selected.weight +  self.get_steps(selected)*5) 
			except Exception as e:
				# ipdb.set_trace()
				pass
			selected.update_weight(new_weight/selected.weight)

	def build(self):
		
		if self.make_dessert:
			self.select_dessert()
		elif ('dairy' , 0) not in self.exclusion_conditions.children:
			self.select_yogurt()

		if self.make_combination:
			self.makeCombinations()
		else:
			self.makeGeneric()
		
		return self

	@property
	def for_random(self):
		return list(filter( lambda x : not bool(x.dessert) , self.selected))

class M4(Base):
	percent = 0.15


	def __init__(self , calories , goal , exclude = "" , extra = 0 , disease = None , exclusion_conditions = None , selected = None):
		self.calories_goal = calories*self.percent + extra
		self.goal = goal
		self.exclusion_conditions = exclusion_conditions 
		self.queryset = Food.m4_objects.exclude(name__in = exclude)

		if self.goal == Goals.WeightLoss:
			self.queryset = self.queryset.filter(for_loss = 1)

		if exclusion_conditions : 
			self.queryset = self.queryset.filter(exclusion_conditions)
		
		self.exclude = exclude
		self.disease = disease
		self.marked = self.queryset
		if disease :
			self.marked = disease.get_queryset(self.queryset)
		self.selected = selected
		self.buildMapper = {
			'drink' : self.select_drink,
			'fruit' : self.select_fruit,
			'salad' : self.select_salad,
			'nuts'  : self.select_nut,
			'snack' : self.select_snacks
		}
		backwardMapper = {
			'pulses' : self.select_snacks,
			'snacks' : self.select_snacks,
			'snaks' : self.select_snacks
		}
		self.buildMapper.update(backwardMapper)

	def select_drink(self):
		calories = 0.15*self.calories_goal
		food_list = self.marked.filter(drink = 1)
		if self.disease == Osteoporosis:
			food_list.filter(Q(name__contains = "Lassi"))
		try:
			self.drink = self.select_best_minimum(food_list , calories , "drink")
		except Exception as e:
			self.drink = random.choice(food_list)
			self.select_item(self.drink , "drink")

	def select_fruit(self , calories = 0 ):
		print("Calling Select Fruit")
		if calories == 0:
			calories = 0.85*self.calories_goal
		self.option = "fruits"
		fruit_items = self.marked.filter(fruit = 1).exclude(name__contains = "Handful")
		self.fruits = self.select_best_minimum(fruit_items , calories , "fruit")
		self.fruits.update_quantity(2)

	def select_salad(self , calories = 0):
		print("Calling Select Salad")
		if calories == 0:
			calories = 0.85*self.calories_goal
		self.option = "salad"
		salad_items = self.marked.filter(salad = 1 ).filter(~Q(name__startswith = "Handful")).all()
		self.salad = self.select_best_minimum(salad_items , calories , "salad")
		self.salad.update_weight(1.5)

	def select_nut(self , calories = 0):
		print("Calling Select Nuts")
		if calories == 0:
			calories = 0.85*self.calories_goal
		self.option = "nuts"
		nuts_items = self.marked.filter(nuts = 1)
		self.nuts = self.select_best_minimum(nuts_items , calories , "nuts")
		self.nuts.update_quantity(2)

	def select_snacks(self , calories = 0):
		print("Calling Select Snacks")
		if calories == 0:
			calories = 0.85*self.calories_goal
		self.option = "snacks"
		snack_items = self.marked.filter(snaks = 1).filter(dessert = 0)
		self.snacks = self.select_best_minimum(snack_items , calories , "snacks")
	def rethink(self):
		selected = getattr(self , self.option)
		if self.option == "fruits" or self.option == "nuts":
			steps = round(self.calories_remaining * selected.quantity/(selected.calarie))
			new_quantity = steps + selected.quantity
			selected.update_quantity(new_quantity/selected.quantity)
		else:
			steps = min( 5 , round(self.calories_remaining * selected.weight/(selected.calarie*10)))
			new_weight = min(250,selected.weight + steps * 10)
			selected.update_weight(new_weight/selected.weight)

	def get_probabilities(self):
		if ("nuts" , 0) in self.exclusion_conditions.children:
			return [1/3,0,1/3,1/3]
		return [0.25 , 0.25 , 0.25 , 0.25]

	def build(self):
		if self.disease and hasattr( self.disease , "m4_build"):
			getattr(self.disease , "m4_build")(self)
		else:
			self.select_drink()
			probability = self.get_probabilities()
			if self.disease and hasattr(self.disease , "nuts_probability"):
				probability = self.disease.nuts_probability
			func = choice([
				self.select_fruit , self.select_nut , self.select_snacks , self.select_salad
			], size = 1 , p = probability)[0]
			if hasattr(self , "drink"):
				cals = self.calories_remaining
			else:
				cals = self.calories_goal * 0.85	
			func(calories = cals)
		return self

class M5(Base):
	percent = 0.20

	def __init__(self , calories , goal , exclude = "" , extra = 0 , disease = None , exclusion_conditions = None , exclude2 = None , make_combination = False , selected = None):
		self.exclusion_conditions = exclusion_conditions
		self.calories_goal = calories*self.percent + extra
		self.goal = goal
		self.disease = disease
		self.exclude = exclude
		self.exclude2 = exclude2
		self.queryset = self.getQuerysetFromGoal()
		self.make_combination = make_combination

		self.queryset = self.queryset.exclude(name__in = exclude).filter(calarie__gt = 0)
		if self.disease:
			self.queryset = self.queryset.filter(self.disease.queryset_filter)

		if exclusion_conditions : 
			self.queryset = self.queryset.filter(exclusion_conditions)

		self.marked = self.queryset
		self.selected = selected

		self.buildMapper = {
			'vegetable' : self.select_vegetables,
			'cereal' : self.select_cereals,
			'pulse' : self.select_pulses,
			'combination' : self.makeCombination
		}
		backwardMapper = {
			'grains_cereals' : self.select_cereals,
			'pulses' : self.select_pulses,
		}
		self.buildMapper.update(backwardMapper)

	def getQuerysetFromGoal(self):
		if self.goal == Goals.WeightLoss : 
			queryset = Food.m5loss_objects
		if self.goal == Goals.WeightGain or self.goal == Goals.MuscleGain:
			queryset = Food.m5gain_objects
		if self.goal == Goals.MaintainWeight:
			queryset = Food.m5stable_objects
		return queryset

	def select_vegetables(self , percent = 0.22):
		calories = percent*self.calories_goal
		self.vegetable_calories = calories
		food_list = self.marked.filter(vegetable = 1).filter(grains_cereals = 0).filter(cuisine = "Generic")
		if self.disease and hasattr(self.disease , "m5_vegetable_filter"):
			food_list = food_list.filter(self.disease.m5_vegetable_filter)
		m = Manipulator(items = food_list , categorizers = [VegetablePulseCategoriser])
		food_list = m.categorize().get_final_list()
		self.vegetable_list = food_list
		self.vegetables = self.select_best_minimum(food_list , calories , "vegetable")


	def select_cereals(self):
		calories = 0.39*self.calories_goal
		if self.exclude2:
			food_list = self.getQuerysetFromGoal().exclude(name__in = self.exclude2).exclude(name__in = self.exclude).filter(grains_cereals = 1).filter(cuisine = "Generic")
			food_list = food_list.filter(self.exclusion_conditions)
		else:
			food_list = self.marked.filter(grains_cereals = 1).filter(cuisine = "Generic")
		if food_list.count() < 1:
			food_list = self.getQuerysetFromGoal().filter(grains_cereals = 1).filter(cuisine = "Generic")
			food_list = food_list.filter(self.exclusion_conditions)
		m = Manipulator(items = food_list , categorizers = [GrainsCerealsCategoriser])
		final_food_list = m.categorize().get_final_list()
		# ipdb.set_trace()
		self.cereals = self.select_best_minimum(final_food_list , calories , "cereal")

	def select_pulses(self , percent = 0.39):
		calories = percent * self.calories_goal
		food_list = self.marked.filter(pulse = 1).filter(grains_cereals = 0).filter(cuisine = "Generic")
		m = Manipulator(items = food_list , categorizers = [VegetablePulseCategoriser])
		food_list = m.categorize().get_final_list()
		self.pulse = self.select_best_minimum(food_list , calories , "pulse")

	def makeGeneric(self):
		self.select_cereals()
		
		if self.cereals.vegetables == 1 and self.cereals.pulse == 0:
			self.select_pulses(percent = 0.61)
		elif self.cereals.vegetables == 0 and self.cereals.pulse == 1:
			self.select_vegetables(percent = 0.61)
		elif self.cereals.vegetables == 1 and self.cereals.pulse == 1:
			self.select_pulses(percent = 0.61)
		if self.cereals.vegetables == 0 and self.cereals.pulse == 0:
			self.select_pulses()
			self.select_vegetables()	
		return self

	def makeCombination(self):
		food_list = self.marked.filter(cuisine = "Combination")
		self.combination = self.select_best_minimum(food_list , self.calories_goal , name = "combination")
	
	def rethink(self):
		if not hasattr(self , "combination"):
			if self.calories < self.calories_goal:
				new_weight = min(self.pulse.weight +  self.get_steps(self.pulse)*5) 
				self.pulse.update_weight(new_weight/self.pulse.weight)

	def build(self):
		if self.make_combination:
			self.makeCombination()
		else:
			self.makeGeneric()
		return self