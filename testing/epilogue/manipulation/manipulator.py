from epilogue.models import Food , FoodTypeSizes

class Manipulator():
	
	def __init__(self , items = [] , categorizer):
		self.items = items
		self.categorizer = categorizer
		self.categorized_data = {}

	def categorize(self):
		