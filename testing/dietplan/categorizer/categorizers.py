from . import filters

class BiryaniCategoriser(filters.BaseFilter):
	
	filters = [
		filters.veg_biryani_filter,
		filters.non_veg_biryani_filter	
	]
class RiceCategoriser(filters.BaseFilter):

	filters = [
		filters.rice_pulao_filter
	]
class RotiCategoriser(filters.BaseFilter):
	filters = [
		filters.roti_filter,
	]

class ParanthaCategoriser(filters.BaseFilter):
	filters = [
		filters.plain_parantha_filter,
		filters.stuffed_parantha_filter,
		filters.roti_filter
	]
class GrainsCerealsCategoriser(filters.BaseFilter):
	'''
	To be used in select_cereals
	'''
	filters = [
		filters.veg_biryani_filter,
		filters.non_veg_biryani_filter,
		filters.rice_pulao_filter,
		filters.roti_filter,
		filters.plain_parantha_filter,
		filters.stuffed_parantha_filter
	]

class DrinkCategoriser(filters.BaseFilter):
	'''
	To be used in M1 , M2 and M4
	'''
	filters = [
		filters.tea_coffee_filter,
		filters.drink_filter
	]

class VegetablePulseCategoriser(filters.BaseFilter):
	'''
	To be used in selecting Vegetables
	'''	

	#List of filters that need to be applied to the item. 
	# They are Processed in the Order of precedence
	# The first one which matches true is returned
	filters = [
		filters.gravy_filter,
		filters.vegetable_filter,
	]

class CombinationCategoriser(filters.BaseFilter):
	filters = [
		filters.khichdi_filter,
		filters.veg_biryani_filter,
		filters.non_veg_biryani_filter
	]

class YogurtCategoriser(filters.BaseFilter):
	filters = [
		filters.yogurt_filter
	]