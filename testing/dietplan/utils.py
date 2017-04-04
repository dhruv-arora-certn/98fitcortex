from .goals import Goals
import itertools , heapq
import numpy as np

def mark_squared_diff(item , pi):
	item.p = item.protein / (pi[0]*item.calarie/4)
	item.c = item.carbohydrates / (pi[1] * item.calarie/4)
	item.f = item.fat / (pi[2] * item.calarie / 9)
	item.pcf = item.p+item.c+item.f
	item.squared_diff = (item.pcf - 3)**2
	return item

def mark_exp_diff(item , pi):
	item._p = (item.protein / (pi[0]*item.calarie/4))
	item.p = item._p*np.exp(np.sign(item._p)*(item._p-1))

	item._c = (item.carbohydrates / (pi[1] * item.calarie/4))
	item.c = item._c
	
	item._f = (item.fat / (pi[2] * item.calarie / 9))
	item.f = item._f*np.exp(np.sign(item._f)*(item._f-1))
	
	item.pcf = item.p+item.c+item.f
	item.squared_diff = np.square(item.pcf - 3)
	return item

def annotate_food(food_queryset , goal ):
	return map( mark_exp_diff , food_queryset , itertools.repeat(goal.get_attributes()))