from . import filters


class VegetablePulseCategoriser(filters.BaseFilter):
	

	#List of filters that need to be applied to the item. 
	# They are Processed in the Order of precedence
	# The first one which matches true is returned
	filters = [
		filters.gravy_filter,
		filters.vegetable_filter,
	]

	def __init__(self , item):
		self.item = item