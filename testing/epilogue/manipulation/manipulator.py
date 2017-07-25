from epilogue.models import Food , FoodTypeSizes
from django.db import connection
from dietplan.goals import Goals
import lego
import itertools

def flatten(v):
	for e in v:
		yield e

class DummyFood:
	'''
	Class To Contain Dummy Food objects after cross join
	'''
	def __init__(self , id , name , size , weight ,nuts ,vegetables , pulse ,squared_diff_weight_loss , squared_diff_weight_gain , squared_diff_weight_maintain , calorie , protein , fat , carbohydrates):
		self.id = id
		self.name = name
		self.size = size
		self.weight = weight
		self.squared_diff_weight_maintain = squared_diff_weight_maintain
		self.squared_diff_weight_gain = squared_diff_weight_gain
		self.squared_diff_weight_loss = squared_diff_weight_loss
		self.calorie = calorie
		self.fat = fat
		self.protein = protein
		self.carbohydrates = carbohydrates
		self.nuts = nuts
		self.quantity = -1
		self.vegetables = vegetables
		self.pulse = pulse

	def __str__(self):
		return self.name

	def __repr__(self):
		return "<" + self.__class__.__name__ + ": " +self.name +" >"

class Manipulator():
	
	def __init__( self , items = [] , categorizers = [] , goal = Goals.WeightLoss):
		self.items = items
		self.categorizers = categorizers
		self.categorized_data = {
			'uncategorized' : []
		}
		self.goal = goal
		self.data = []

	def categorize(self):
		m = [map(e.categorize , self.items) for e in self.categorizers]
		a = itertools.chain(*m)
		for e in a:
			x,y = e.popitem()
			if self.categorized_data.get(x):
				self.categorized_data[x].append(y)
			else:
				self.categorized_data[x] = []
				self.categorized_data[x].append(y)
		return self

	@property
	def types(self):
		l = set(self.categorized_data.keys())
		return l - {'uncategorized',}

	def idsToString(self , ids):
		return ','.join(str(e) for e in ids)

	def query_string(self , ids , type_):
		string = '''
		select 
			t2.id , 
			t2.name, 
			t1.size , 
			t1.weight ,
			t2.nuts,
			t2.vegetables,
			t2.pulse,
			t2.squared_diff_weight_loss ,
			t2.squared_diff_weight_gain ,
			t2.squared_diff_weight_maintain,
			round(t2.calorie_unit*t1.weight,2) as calorie , 
			round(t2.protein_unit*t1.weight,2) as protein , 
			round(t2.fat_unit*t1.weight,2) as fat,
			round(t2.carb_unit*t1.weight,2) as carbs 
		from food_type_sizes t1 cross join ( 
				select * from business_diet_list 
				where id in (%s) 
				order by %s
		) as t2
		where t1.type="%s"
		order by t2.id''' % (self.idsToString(ids)  , self.goal.field , type_ )
		return string

	def get_results(self , query):
		cursor = connection.cursor()
		cursor.execute(query)
		return cursor.fetchall()

	def cross_join(self):
		for e in self.types:
			ids = [a.id for a in self.categorized_data[e]]
			qs = self.query_string(ids , e)
			self.data.extend(self.get_results(qs))				
		return self

	def iter_objs(self):
		for e in itertools.chain(self.categorized_data['uncategorized'] , self.data ):
			if isinstance(e , tuple):
				yield DummyFood(*e)
			else :
				yield e
	def get_final_list(self):
		self.cross_join()
		self.data_list = list(self.iter_objs())
		return self.data_list