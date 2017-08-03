def veg_filter(x): 
	return not bool(x.non_veg) 

def non_veg_filter(x):
	return bool(x.non_veg) 

def combination_filter(x): 
	return x.cuisine == "Combination"

def biryani_filter(x) : 
	return combination_filter(x) and "biryani" in x.name.lower()

def vegetable_filter(x) : 
	return x.vegetable == 1

vegetable_filter.name = "vegetable"

def gravy_filter(x): 
	return x.pulses ==  1
gravy_filter.name = "pulses"

tea_coffee_filter = lambda x : x.drink == 1 and x.size ==  "Teacup"
tea_coffee_filter.name = "beverage"

rice_pulao_filter = lambda x : x.grains_cereals == 1 and x.size == "Quarter Plate" and x.wheat == 0
rice_pulao_filter.name = "rice_pulao"

roti_filter = lambda x : x.grains_cereals == 1 and (x.size == "Pieces" or x.size == "Piece")
roti_filter.name = "roti"

khichdi_filter = lambda x : combination_filter(x) and "khichdi" in x.name.lower()
khichdi_filter.name = "khichdi"

veg_biryani_filter = lambda x : biryani_filter(x) and veg_filter(x)
veg_biryani_filter.name = "veg_biryani"

non_veg_biryani_filter = lambda x : biryani_filter(x) and non_veg_filter(x)
non_veg_biryani_filter.name = "non_veg_biryani"

def yogurt_filter(item):
	return item.yogurt == 1
yogurt_filter.name = "yogurt"

def drink_filter(item):
	return item.drink == 1
drink_filter.name = "drink"

def soup_filter(item):
	return drink_filter(item) and item.size == "Soup Bowl"
soup_filter.name = "soup"

def parantha_filter(item):
	return "parantha" in item.name.lower() or "prantha" in item.name.lower() or item.grains_cereals == 1

def plain_parantha_filter(item):
	return  parantha_filter(item) and item.vegetables == 0 and item.pulse == 0 and not non_veg_filter(item) 
plain_parantha_filter.name = "plain_parantha"


def stuffed_parantha_filter(item):
	return item.grains_cereals == 1 and (item.vegetables == 1 or item.pulse == 1 or non_veg_filter(item)) and (item.size.lower().strip() == "piece" or item.size.lower().strip() == "pieces") 
stuffed_parantha_filter.name = "stuffed_parantha"

def soup_filter(item):
	return "soup" in item.name.lower()
soup_filter.name = "soup"

def salad_filter(item):
	return item.salad == 1 
salad_filter.name = "salad"

class BaseFilter():
	'''
	Base class for filters
	'''
	@classmethod
	def get_category(self , item):
		'''
		Return the first category that matches the criteria
		'''
		for e in self.filters:
			if e(item):
				return e.name
		return "uncategorized"

	@classmethod
	def categorize(self , item):
		return {
			self.get_category(item) : item
		}

