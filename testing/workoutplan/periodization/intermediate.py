from django.db.models import Q
import functools

@functools.lru_cache()
def get_intermediate_cardio_periodized(user_week_no):
	return [
		{
			"filter" : Q(exercise_level = "High"),
			"ratio" :1
		}
	]
