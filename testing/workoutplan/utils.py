from workoutplan import levels
from workoutplan.goals import Goals
from collections import namedtuple
from workoutplan import resistance_data
from django.db.models import Q

import random
import ipdb
import collections
import enum

type_list = ["WeightLoss" , "WeightGain" , "MuscleGain" , "MaintainWeight"]

days = namedtuple("Days" , ["cardio","rt","total"])

Novice = namedtuple("Novice" , type_list)
Beginner = namedtuple("Beginner" , type_list)
Intermediate = namedtuple("Intermediate" , type_list)

WeightGain = namedtuple("WeightGain" , ["days"])
WeightLoss = namedtuple("WeightLoss" , ["days"])
MuscleGain = namedtuple("MuscleGain" , ["days"])
MaintainWeight = namedtuple("MaintainWeight" , ["days"])

NoviceDays = Novice(
	WeightLoss(
		days(5,0,5)
	),
	WeightGain(
		days(3,0,3)
	),
	MuscleGain(
		days(4,0,4)
	),
	MaintainWeight(
		days(4,0,4)
	)
)

BeginnerDays = Beginner(
	WeightLoss(
		days(5,2,5)		
	),
	WeightGain(
		days(2,3,5)
	),
	MuscleGain(
		days(2,3,5)
	),
	MaintainWeight(
		days(3,2,5)
	)
)

IntermediateDays = Intermediate(
	WeightLoss(
		days(5,2,5)
	),
	WeightGain(
		days(2,6,6)
	),
	MuscleGain(
		days(2,6,6)
	),
	MaintainWeight(
		days(3,3,5)
	)
)

ct = namedtuple(
	"ConditionalTraining" , ["novice" , "beginner" , "intermediate"]
)

ConditionalTrainingDays = ct(
	NoviceDays , BeginnerDays , IntermediateDays
)


class Luggage:

	def __init__(self , weight , items , key , randomize = True , batchSize = 5):
		self.weight = weight
		self.items = items
		self.key = key
		self.randomize = randomize
		self.packed = set()
		self.batchSize = batchSize

	def pickAndPack(self):
		selectedWeight = sum(getattr(e , self.key) for e in self.packed)
		while selectedWeight < self.weight:
			batch = random.sample(self.items , self.batchSize)

			for e in batch:
				assert isinstance(getattr(e,self.key) , int) , "Not an integer %s - %s"%(getattr(e , self.key) , type(getattr(e , self.key)))
				if selectedWeight + getattr(e , self.key) <= self.weight :
					selectedWeight += getattr(e , self.key)
					self.packed.add(e)
		return self


def get_resistance_filter( user , day_number):
	assert user.level_obj is not levels.Novice

	r =  getattr(user.level_obj.Resistance , user.goal.__name__)
	return getattr(r , "D%s"%(day_number))

def get_days(cls_obj , category):
		goal = cls_obj.user.goal
		if goal == Goals.WeightLoss:
			return getattr(category,"WeightLoss").days

		elif goal == Goals.WeightGain:
			return getattr(category,"WeightGain").days

		elif goal == Goals.MuscleGain:
			return getattr(category,"MuscleGain").days

def get_category_decorator(category):
	def decorator(fn):
		def applyCat(cls_obj):
			return get_days(cls_obj , category)
		return applyCat
	return decorator

filter_tuple = collections.namedtuple("filter_" , ["filter" , "count"])

class CardioStretchingFilter(enum.Enum):
	QUADS = filter_tuple(
		filter = Q(muscle_group_name = "Quadriceps"),
		count = 1
	)
	CHEST = filter_tuple(
		filter = Q(muscle_group_name  = "Chest"),
		count = 1
	)
	GLUTES = filter_tuple(
		filter = Q(muscle_group_name = "Glutes"),
		count = 1
	)
	BACK = filter_tuple(
		filter = Q(muscle_group_name = "Back"),
		count = 1
	)
