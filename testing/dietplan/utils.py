from .goals import Goals
from multiprocessing import Pool
import itertools , heapq
import numpy as np

def mark_squared_diff(item , pi):
	item.p = item.protein / (pi[0]*item.calarie/4)
	item.c = item.carbohydrates / (pi[1] * item.calarie/4)
	item.f = item.fat / (pi[2] * item.calarie / 9)
	item.pcf = item.p+item.c+item.f
	item.squared_diff = (item.pcf - 3)**2
	return item

def mark_exp_diff(args):
	item = args[0]
	pi = args[1]
	item._p = (item.protein / (pi[0]*item.calarie/4))
	item.p = item._p*np.exp(np.sign(item._p)*(item._p-1))

	item._c = (item.carbohydrates / (pi[1] * item.calarie/4))
	item.c = item._c
	
	item._f = (item.fat / (pi[2] * item.calarie / 9))
	item.f = item._f*np.exp(np.sign(item._f)*(item._f-1))
	print(pi[3])	
	item.pcf = item.p+item.c+item.f
	try:
		setattr(item , pi[3] , np.square(item.pcf - 3))
		item.save()
	except Exception as e:
		print(item.p , item.c , item.f , item.pcf)
		print(item._p , item._c , item._f)
		print("Error is " , e)
	return item

def annotate_food(food_queryset , goal ):

	data = map( mark_exp_diff , zip(food_queryset , itertools.repeat(goal.get_attributes())))
	return data
