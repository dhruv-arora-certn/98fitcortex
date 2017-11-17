
from .beginner import get_beginner_cardio_periodized
from .novice import get_novice_cardio_periodized
from .intermediate import get_intermediate_cardio_periodized

from workoutplan import levels

import functools

@functools.lru_cache()
def get_cardio_periodized(level , user_week_no):

	if level == levels.Beginner:
		return get_beginner_cardio_periodized(user_week_no)

	elif level == levels.Intermediate:
		return get_intermediate_cardio_periodized(user_week_no)

	elif level == levels.Novice:
		return get_novice_cardio_periodized(user_week_no)
