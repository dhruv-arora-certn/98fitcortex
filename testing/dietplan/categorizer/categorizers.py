from . import filters


class VegetablePulseCategoriser(filters.BaseFilter):
	

	#List of filters that need to be applied to the item. 
	# They are Processed in the Order of precedence
	# The first one which matches true is returned
	filters = [
		filters.gravy_filter,
		filters.vegetable_filter,
	]

class TeaCoffeeCategoriser(filters.BaseFilter):

	filters = [
		filters.tea_coffee_filter
	]


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

class GrainsCerealsCategoriser(filters.BaseFilter):
	filters = [
		filters.veg_biryani_filter,
		filters.non_veg_biryani_filter,
		filters.rice_pulao_filter,
		filters.roti_filter,
		filters.parantha_filter
	]