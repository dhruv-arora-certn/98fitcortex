from . import constants

from epilogue.utils import get_week , get_year

import itertools

def get_window_tuples(week = get_week() , year = get_year()):
	return [
		(w , y) for w,y in zip(
			[
				week + i for i in range(1, 1 + constants.REGENERATION_WINDOW)
			],
			itertools.repeat(year , constants.REGENERATION_WINDOW)
		)
	]


def create_regeneration_node(_type , year , week):
	pass

def create_diet_regeneration_node(year,week):
	return create_regeneration_node(
		"diet" , year , week
	)

def create_workout_regeneration_node(year,week):
	return create_regeneration_node(
		"workout" , year , week
	)
