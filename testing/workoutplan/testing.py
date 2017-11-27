from workoutplan import levels
from workoutplan.goals import Goals
from workoutplan.generator import Generator

from django.core.cache import cache

import random
import itertools
import logging
import ipdb

logger = logging.getLogger(__name__)
logger.addHandler(logging.FileHandler("info.log"))
logger.setLevel(logging.INFO)


class LevelTest:

	def is_novice(self):
		return  self.level_obj == levels.Novice

	def is_beginner(self):
		return self.level_obj == levels.Beginner

	def is_intermediate(self):
		return self.level_obj == levels.Intermediate

def dummy_customer(level , goal , user_workout_week):
	return type(
		"DummyCustomer",
		(LevelTest,),
		{
			"level_obj" : level,
			"goal" : goal,
			"user_relative_workout_week" : user_workout_week,
			"id" : random.randint(9,100),
			"email" : "test@98fit.com"

		}
	)()

def novice_week():
	return range(1,7)

def beginner_week():
	return range(1,17)

def intermediate_week():
	return range(1, 20)

def generate_random_diet_plan():
	goals = [Goals.WeightLoss , Goals.WeightGain , Goals.MaintainWeight , Goals.MuscleGain]
	lvls = [levels.Beginner ]
	weeks = beginner_week()
	return itertools.product(lvls , goals, [1])
	generated = []
	for e in itertools.product(lvls , goals , weeks):
		try:
			c = dummy_customer(*e)
			g = Generator(c)
			g.generate()
			key = "workout_%s_%s_%d"%(e[0].__name__ , e[1].__name__ , e[2])
			cache.set(key , g.weekly_as_dict())
			generated.append(g.weekly_as_dict())
		except Exception as err:
			logger.info("="*30)
			logger.info("Error for params %s : %s : %s"%(e[0].__name__ , e[1].__name__ , e[2]))
			logger.info("Error is %s"%err)
			ipdb.set_trace()
			raise err
	return generated
