from workoutplan import levels
from dietplan.goals import Goals
from collections import namedtuple

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
		days(5,None,5)
	),
	WeightGain(
		days(3,None,3)
	),
	MuscleGain(
		days(4,None,4)
	),
	MaintainWeight(
		days(4,None,4)
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


