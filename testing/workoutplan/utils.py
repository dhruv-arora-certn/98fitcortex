from workoutplan import levels
from dietplan.goals import Goals
from collections import namedtuple
import random

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
				if selectedWeight + getattr(e , self.key) <= self.weight :
					selectedWeight += getattr(e , self.key)
					self.packed.add(e)
		return self


ResistanceFilter = namedtuple("ResistanceFilters" , ["filters"])
ResistanceFilterContainer = namedtuple("ResistanceFilterContainer" , ["day" , "filters"])
