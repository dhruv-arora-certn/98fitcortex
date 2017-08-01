def veg_filter(x): 
	return x.poultary == 0 and x.seafood == 0 and x.pork == 0 and x.meat == 0 and x.lamb_mutton == 0 and x.beef == 0 and x.other_meat == 0 and x.egg == 0

def non_veg_filter(x):
	return x.poultary == 0 or x.seafood == 0 or x.pork == 0 or x.meat == 0 or x.lamb_mutton == 0 or x.beef == 0 or x.other_meat == 0 or x.egg == 0

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

roti_filter = lambda x : x.grains_cereals == 1 and ("roti" in x.name.lower() or "chapati" in x.name.lower()) and (x.size == "Pieces" or x.size == "Piece")
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
	return  parantha_filter(item) and item.vegetable == 0 and item.pulse == 0 and item.egg == 0
plain_parantha_filter.name = "plain_parantha"


def stuffed_parantha_filter(item):
	return parantha_filter(item) and not plain_parantha_filter(item)
stuffed_parantha_filter.name = "stuffed_parantha"

def soup_filter(item):
	return "soup" in item.name.lower()
soup_filter.name = "soup"

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

