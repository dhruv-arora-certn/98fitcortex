from epilogue.models import Food , FoodTypeSizes

class Manipulator():
	
	def __init__( self , items = [] , categorizers = [] ):
		self.items = items
		self.categorizers = categorizers
		self.categorized_data = {}

	def categorize(self):
		m = [map(e.categorize , self.items) for e in self.categorizers]
		for e in m:
			self.categorized_data.update(e)
					