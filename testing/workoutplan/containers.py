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
