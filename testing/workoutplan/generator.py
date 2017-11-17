from . import levels
from .goals import Goals
from .utils import NoviceDays , BeginnerDays , IntermediateDays , days as namedDays ,  get_resistance_filter , get_category_decorator
from .day import ExerciseDay
from . import shared_globals

import random
import logging
import sys
import os
import itertools

class ResistanceDistribution:

    def __init__(self , user , day , day_number):
        self.user = user
        self.day = day
        self.day_number = day_number

class Generator():

	def __init__(self, user):
		self.logger = logging.getLogger('workoutplan.generator')
		self.user =  user
		self.conditional_days = self.get_conditional_days()
		self.get_resistance_distribution()
		self.logger.info("Starting Workout Generator for user %s-%d"%(self.user.email , self.user.id))

	@get_category_decorator(NoviceDays)
	def _get_novice_days(self):
		pass

	@get_category_decorator(BeginnerDays)
	def _get_beginner_days(self):
		pass

	@get_category_decorator(IntermediateDays)
	def _get_intermediate_days(self):
		pass

	@classmethod
	def _get_days_distribution(self, days):
		'''
		@days is a namedtuple instance with cardio , rt and total.
		#Notes
		Ideally should be a utility function, but i realized that after writing it and as of right now, too lazy to move it out. Hence
		a classmethod
		'''
		day_range =  {1,2,3,4,5}
		cardio_days = set(random.sample(
			day_range,
			days.cardio
		))
		if days.total <= days.cardio + days.rt:
			rt_days = random.sample(day_range , days.rt)
		else:
			rt_days = random.sample(day_range.difference(cardio_days) , days.rt)

		return cardio_days , set(rt_days)

	def get_resistance_distribution(self):

		rt_days = self.conditional_days.rt
		dist = {}

		if rt_days:
			for i,e in enumerate(rt_days):
				f = get_resistance_filter(self.user , i+1)
				dist[e] = f

		self.resistance_distribution = dist
		return dist

	def get_conditional_days(self):
		'''
		Number of Cardio Days for the user
		'''
		if self.user.level_obj == levels.Novice:
			days = self._get_novice_days()
		elif self.user.level_obj == levels.Beginner:
			days = self._get_beginner_days()
		elif self.user.level_obj == levels.Intermediate:
			days = self._get_intermediate_days()
		cardio_days , rt_days = self._get_days_distribution(days)
		data = namedDays(cardio_days , rt_days , days.total)
		shared_globals.conditional_days = data
		return data

	def get_resistance_filter_for_day(self , day):
		return self.resistance_distribution.get(day)

	def should_make_cardio(self , day):
		return day in self.conditional_days.cardio

	def _generate(self):
		days = {1,2,3,4,5}
		for e in days:
			resistance_filter = self.get_resistance_filter_for_day(e)
			make_cardio = self.should_make_cardio(e)
			d = ExerciseDay(e , self.user , make_cardio = make_cardio , resistance_filter = resistance_filter)
			setattr(self , "D%s"%e , d)
			d.build()
		return self

	def weekly_as_dict(self):
		days = [1,2,3,4,5]
		lists = ["warmup" , "main" , "stretching" , "cooldown"]
		data = {}
		for d,l in zip(days , itertools.repeat(lists)):
			data[d] = {}
			day_obj = getattr(self , "D%d"%d)
			day_data = (getattr(day_obj , e) for e in l)
			[data[d].update(**getattr(o , "selected")) for o in day_data]
		return data

	def generate(self ):
		self._generate()
		return self
		try:
			self._generate()
		except Exception as e:
			exc_type , exc_obj , exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			self.logger.info("Error Generating Workout Plan: %s %s %s"%(exc_type , fname , exc_tb.tb_lineno))
		else:
			self.logger.info("Workout Successfully Generated for user")
		return self
