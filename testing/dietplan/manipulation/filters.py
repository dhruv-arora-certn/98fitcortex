vegetable_filter = lambda x : x.vegetable == 1
gravy_filter = lambda x: x.pulses ==  1
tea_coffee_filter = lambda x : x.drink == 1 and x.size ==  "Teacup"

vegetable_filter.name = "vegetable"
gravy_filter.name = "pulses"
tea_coffee_filter.name = "beverage"


class BaseFilter():
	'''
	Base class for filters
	'''
	def get_category(self):
		'''
		Return the first category that matches the criteria
		'''
		for e in self.filters:
			if e(self.item):
				return e.name
		return None

	def iget_category(self):
		mapper = lambda x : x.name if x(self.item) else False
		f = filter(mapper , self.filters)
		while True:
			a = next(f)
			return a

