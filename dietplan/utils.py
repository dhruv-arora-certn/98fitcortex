from .goals import Goals
import itertools , heapq

def mark_squared_diff(item , pi):
	p = item.protein / (pi[0]*item.calorie/4)
	c = item.carbohydrates / (pi[1] * item.calorie/4)
	f = item.fat / ( pi[2] * item.calorie / 9)
	item.pcf = p+c+f
	item.squared_diff = (item.pcf - 3)**2
	return item

def annotate_food(food_queryset , goal ):
	print("Enter")
	if goal == Goals.WeightLoss:
		print("True")
		return map( mark_squared_diff , food_queryset , itertools.repeat([ Goals.WeightLoss.protein , Goals.WeightLoss.carbs , Goals.WeightLoss.fat ]) )
	if goal == Goals.WeightGain:
		return map( mark_squared_diff , food_queryset , itertools.repeat([ Goals.WeightGain.protein , Goals.WeightGain.carbs , Goals.WeightGain.fat ]) )
	
	if goal == Goals.MaintainWeight:
		return map( mark_squared_diff , food_queryset , itertools.repeat([ Goals.MaintainWeight.protein , Goals.MaintainWeight.carbs , Goals.MaintainWeight.fat ]) )

	if goal == Goals.MuscleGain:
		return map( mark_squared_diff , food_queryset , itertools.repeat([ Goals.MuscleGain.protein , Goals.MuscleGain.carbs , Goals.MuscleGain.fat ]) )