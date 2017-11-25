from .nomenclature import UpperBody , LowerBody
from django.db.models import Q

class ChestAndBackFilter():
	filters = [
				{
					"filter" : UpperBody.chest() & Q(exercise_type = "Isolated"),
					"count" : 3,
				},
				{
					"filter" : UpperBody.back() & Q(exercise_type = "Isolated"),
					"count" : 3,
				}
			]
	chest = {
					"filter" : UpperBody.chest(),
					"count" : 5,
			}

class ShouldersAndArmsFilter():
	filters = [
				{
					"filter" : UpperBody.shoulder(),
					"count" : 3
				},
				{
					"filter" : UpperBody.biceps(),
					"count" : 1
				},
				{
					"filter" : UpperBody.triceps(),
					"count" : 1
				},
				{
					"filter" : Q(exercise_type = "Compound") & Q(body_part = "Upper"),
					"count" : 1
				}
			]

class AbdomenAndLegsFilter():
	filters = [
				{
					"filter" : UpperBody.abdomen() & Q(exercise_type = "Isolated"),
					"count" : 3
				},
				{
					"filter" : LowerBody.hamstrings() & Q(exercise_type = "Isolated"),
					"count" : 1
				},
				{
					"filter" : LowerBody.quadriceps(),
					"count" : 1
				},
				{
					"filter" : Q(body_part = "Lower") & Q(exercise_type = "Compound") ,
					"count" : 1
				}
			]

class UpperBodyFilter():
	filters = [

					{
						"filter" : i(),
						"count" : e
					}
					for i,e in UpperBody.groups()

			]

class LowerBodyFilter():
	filters = [
				{
					"filter" : i,
					"count" : e
				}
				for i,e in LowerBody.groups()
			]

