import functools
import collections
import enum

from django.db.models import Q

filter_tuple = collections.namedtuple("filter_tuple" , ["filter" , "ratio"])


@functools.lru_cache()
def get_beginner_cardio_periodized(relative_week ):

	#assert user_week_no >= 7 and user_week_no <= 24 , "Beginner week no is between 7 and 24"

	if 1 <= relative_week <= 3:
		return [
			{
				"filter" : Q(exercise_level = "Moderate") ,
				"ratio" : 0.85
			},
			{
				"filter" : Q(exercise_level = "High"),
				"ratio" : 0.15
			}
		]
	elif 4 <= relative_week <= 6:
		return [
			{
				"filter" : Q(exercise_level = "Moderate"),
				"ratio" : 0.75
			},
			{
				"filter" : Q(exercise_level = "High"),
				"ratio" : 0.25
			}
		]
	elif 7 <= relative_week <= 9:
		return [
			{
				"filter" : Q(exercise_level = "Moderate"),
				"ratio" : 0.60
			},
			{
				"filter" : Q(exercise_level = "High"),
				"ratio" : 0.40
			}
		]
	elif 10 <= relative_week <= 12:
		return [
			{
				"filter" : Q(exercise_level = "Moderate"),
				"ratio" : 0.5
			},
			{
				"filter" : Q(exercise_level = "High"),
				"ratio" : 0.5
			}
		]
	elif 13 <= relative_week <= 15:
		return [
			{
				"filter" : Q(exercise_level = "Moderate"),
				"ratio" : 0.4
			},
			{
				"filter" : Q(exercise_level = "High"),
				"ratio" : 0.6
			}
		]
	elif 16 <= relative_week <= 18:
		return [
			{
				"filter" : Q(exercise_level = "Moderate"),
				"ratio" : 0.3
			},
			{
				"filter" : Q(exercise_level = "High"),
				"ratio" : 0.7
			}
		]
