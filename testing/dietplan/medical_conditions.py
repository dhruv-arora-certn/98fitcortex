from django.db.models import Q
from epilogue.models import Food

class Base:
	def __init__(self , meal = None):
		self.meal = meal
	
	@classmethod	
	def get_queryset(self , queryset):
		return queryset.filter(self.queryset_filter)

class Osteoporosis(Base):

	queryset_filter = ~Q(name__icontains = "Soda") & ~Q(name__icontains = "Tea")& ~Q(name__icontains = "Chai") & ~Q(name__icontains = "Coffee")
	@classmethod
	def m4_build(self , meal):
		items = Food.objects.filter(Q(name__icontains = "soya") | Q(name__icontains = "tofu")).exclude(name__in = meal.exclude)
		meal.osteo = meal.select_best_minimum(items , meal.calories_goal , "osteo_snack")
		meal.osteo.update_weight(0.4 * meal.calories_goal / meal.osteo.weight)
		meal.option = "osteo"
		drinks = Food.objects.filter(Q(name__contains = "Lassi")).exclude(name__in = meal.exclude)
		meal.drink = max( drinks.all() , key= lambda x : x.calcium)
		meal.drink.update_weight(0.6 * meal.calories_goal / meal.drink.weight)
		meal.select_item(meal.drink) 
