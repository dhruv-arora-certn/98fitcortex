from .nomenclature import UpperBody , LowerBody
from django.db.models import Q

def isolated():
	return Q(exercise_type = "Isolated")

class ChestAndBackFilter():
	filters = [
				{
					"filter" : Q(muscle_group_name = "Chest") & Q(exercise_type = "Isolated"),
					"count" : 3,
					"stretching_count" : 2
				},
				{
					"filter" : Q(muscle_group_name = "Back") & isolated(),
					"count" : 3,
					"stretching_count" : 2
				}
			]
	chest = {
					"filter" : UpperBody.chest() & Q(exercise_type = "Isolated"),
					"count" : 5,
			}

class ShouldersAndArmsFilter():
	filters = [
				{
					"filter" : Q(muscle_group_name__icontains = "shoulder") & isolated(),
					"count" : 3
				},
				{
					"filter" : Q(muscle_group_name = "Biceps") & isolated(),
					"count" : 1
				},
				{
					"filter" : Q(muscle_group_name = "Triceps") & isolated(),
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

