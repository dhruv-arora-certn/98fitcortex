from . import levels
from .goals import Goals
from .utils import NoviceDays , BeginnerDays , IntermediateDays , days as namedDays ,  get_resistance_filter , get_category_decorator
from .day import ExerciseDay
import random

class ResistanceDistribution:

    def __init__(self , user , day , day_number):
        self.user = user
        self.day = day
        self.day_number = day_number

class Generator():

	def __init__(self, user):
		self.user =  user
		self.conditional_days = self.get_conditional_days()
		self.get_resistance_distribution()

	@get_category_decorator(NoviceDays)
	def _get_novice_days(self):

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
		day_range =  {1,2,3,4,5,6,7}
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
		return namedDays(cardio_days , rt_days , days.total)

	def get_resistance_filter_for_day(self , day):
		return self.resistance_distribution.get(day)

	def should_make_cardio(self , day):
		return day in self.conditional_days.cardio

	def generate(self):
		days = {1,2,3,4,5,6,7}

		for e in days:
			resistance_filter = self.get_resistance_filter_for_day(e)
			make_cardio = self.should_make_cardio(e)
			d = ExerciseDay(e , self.user , make_cardio = make_cardio , resistance_filter = resistance_filter)
			setattr(self , "d%s"%e , d)

