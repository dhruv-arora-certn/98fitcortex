from dietplan.goals import Goals
from django.db import models

QUANTITY_MANIPULATE = [
	"Parantha",
	"Roti",
	"Dosa",
	"Cheela",
	"Uttapam"
]
UNCHANGABLE_ITEMS = [
	'Boiled Egg White',
	'Salad'
]
fieldMapper = {
		Goals.WeightLoss : "squared_diff_weight_loss",
		Goals.MaintainWeight : "squared_diff_weight_maintain",
		Goals.WeightGain : "squared_diff_weight_gain",
		Goals.MuscleGain : "squared_diff_muscle_gain"
}

exclusionMapper = {
	'wheat' : models.Q(wheat = 0),
	'nuts' : models.Q(nuts = 0),
	'nut' : models.Q(nut = 0),
	'dairy' : models.Q(dairy = 0),
	'lamb_mutton' : models.Q(lamb_mutton = 0),
	'beef' : models.Q(dairy = 0),
	'seafood' : models.Q(seafood = 0),
	'poultary' : models.Q(poultary = 0),
	'meat' : models.Q(meat = 0),
	'egg' : models.Q(egg = 0)
}
food_category_exclusion_mapper = {
	'veg' : models.Q(poultary = 0) & models.Q(seafood = 0) & models.Q(pork = 0) & models.Q(meat = 0) & models.Q(lamb_mutton = 0) & models.Q(beef = 0) & models.Q(other_meat = 0) & models.Q(egg = 0),
	'nonveg' : models.Q(),
	'egg' : models.Q(poultary = 0) & models.Q(seafood = 0) & models.Q( pork = 0) & models.Q(meat = 0) & models.Q( lamb_mutton = 0) & models.Q(beef = 0) & models.Q(other_meat = 0)	
}