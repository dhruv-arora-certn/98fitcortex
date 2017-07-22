from epilogue.models import Food , FoodTypeSizes
from django.db.models import connection
import lego
import itertools

class DummyFood:
	'''
	Class To Contain Dummy Food objects after cross join
	'''
	@lego.assemble
	def __init__(self , *args , **kwargs):
		pass

class Manipulator():
	
	def __init__( self , items = [] , categorizers = [] ):
		self.items = items
		self.categorizers = categorizers
		self.categorized_data = {}

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
		return l - set(['uncategorized'])
					