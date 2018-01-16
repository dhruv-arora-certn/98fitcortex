from . import constants
from . import models

from epilogue.models import GeneratedDietPlan
from epilogue.utils import get_week , get_year

from workout.models import GeneratedExercisePlan

import itertools
import logging


def get_logger():
	return logging.getLogger(__name__)

def get_window_tuples(week = get_week() , year = get_year()):
	return [
		(y , w) for w,y in zip(
			[
				week + i for i in range(0, 1 + constants.REGENERATION_WINDOW)
			],
			itertools.repeat(year , constants.REGENERATION_WINDOW + 1)
		)
	]


def create_regeneration_node(_type, user, year , week):
	logger = get_logger()
	logger.debug("++++++++++++++++ Creating Object")
	obj = models.RegenerationLog.objects.get_or_create(
		type = _type,
		year = year,
		week = week,
		customer = user
	)
	return obj

def create_diet_regeneration_node(user,year,week):
	logger = get_logger()
	dietplan = GeneratedDietPlan.objects.filter(
		year = year,
		week_id = week,
		customer = user
	)
	count = dietplan.count()
	logger.debug("Reaching Diet Regeneration Stage count:%d , week:%d , year:%d"%(count,week,year))
	logger.debug(str(dietplan.query))
	if count:
		return create_regeneration_node(
			"diet" ,user ,year , week
		)
	return None

def create_workout_regeneration_node(user,year,week):
	logger = get_logger()
	logger.debug("Reaching Workout Regeneration Stage")

	workoutplan = GeneratedExercisePlan.objects.filter(
		year = year,
		week_id  = week,
		customer = user
	)
	if workoutplan.count():
		return create_regeneration_node(
			"workout" , user ,year , week
		)
	return None
