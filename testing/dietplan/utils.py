from .goals import Goals
import itertools , heapq

def mark_squared_diff(item , pi):
	s = sum(pi)
	item.p = item.protein / (pi[0]*item.calarie/4)
	item.c = item.carbohydrates / ((pi[1]/s) * item.calarie/4)
	item.f = item.fat / ( (pi[2]/s) * item.calarie / 9)
	item.pcf = item.p+item.c+item.f
	item.squared_diff = (item.pcf - 3)**2
	return item

def annotate_food(food_queryset , goal ):
	if goal == Goals.WeightLoss:
		return map( mark_squared_diff , food_queryset , itertools.repeat([ Goals.WeightLoss.protein , Goals.WeightLoss.carbs , Goals.WeightLoss.fat ]) )
	if goal == Goals.WeightGain:
		return map( mark_squared_diff , food_queryset , itertools.repeat([ Goals.WeightGain.protein , Goals.WeightGain.carbs , Goals.WeightGain.fat ]) )
	
	if goal == Goals.MaintainWeight:
		return map( mark_squared_diff , food_queryset , itertools.repeat([ Goals.MaintainWeight.protein , Goals.MaintainWeight.carbs , Goals.MaintainWeight.fat ]) )

	if goal == Goals.MuscleGain:
		return map( mark_squared_diff , food_queryset , itertools.repeat([ Goals.MuscleGain.protein , Goals.MuscleGain.carbs , Goals.MuscleGain.fat ]) )