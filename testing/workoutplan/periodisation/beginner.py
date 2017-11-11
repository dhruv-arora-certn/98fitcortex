import functools
import collections
import enum

from django.db.models import Q

filter_tuple = collections.namedtuple("filter_tuple" , ["filter" , "ratio"])


class BeginnerCardio(enum.Enum):
	pass
@functools.lru_cache()
def get_beginner_cardio_periodized(user_week_no ):
	assert user_week_no >= 7 and user_week_no <= 24 , "Beginner week no is between 7 and 24"
	relative_week = user_week_no -  7 + 1


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
