from . import levels
from .goals import Goals
<<<<<<< HEAD
from .utils import NoviceDays , BeginnerDays , IntermediateDays , days as namedDays , ResistanceFilterContainer , ResistanceFilter , get_resistance_filter
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

	def _get_novice_days(self):
=======
from .utils import NoviceDays , BeginnerDays , IntermediateDays , days as namedDays
import random

class Generator():

	def __init__(self, user):
		self.user =  user 
		self.conditional_days = self.get_conditional_days()

	def _get_novice_days(self):	

		goal = self.user.goal
		if goal == Goals.WeightLoss:
			return NoviceDays.WeightLoss.days
		elif goal == Goals.WeightGain:
			return NoviceDays.WeightGain.days
		elif goal == Goals.MuscleGain:
			return NoviceDays.MuscleGain.days

	def _get_beginner_days(self):

		goal = self.user.goal
		if goal == Goals.WeightLoss:
			return BeginnerDays.WeightLoss.days

		elif goal == Goals.WeightGain:
			return BeginnerDays.WeightGain.days

		elif goal == Goals.MuscleGain:
			return BeginnerDays.MuscleGain.days


	def _get_intermediate_days(self):

		goal = self.user.goal
		if goal == Goals.WeightLoss:
			return IntermediateDays.WeightLoss.days

		elif goal == Goals.WeightGain:
			return IntermediateDays.WeightGain.days

		elif goal == Goals.MuscleGain:
			return IntermediateDays.MuscleGain.days

<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 1f1a621578ff8fcfdd7ede4cfcc91f9254c0e278
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

		return cardio_days , rt_days

<<<<<<< HEAD
	def get_resistance_distribution(self):
		rt_days = self.conditional_days.rt

		if rt_days:
			for i,e in enumerate(rt_days):
				f = get_resistance_filter(user , i+1)
	def get_conditional_days(self):
		'''
		Returns a namedtuple with a list of cardio days and list of rt days
=======

	def get_conditional_days(self):
		'''
		Number of Cardio Days for the user
>>>>>>> 1f1a621578ff8fcfdd7ede4cfcc91f9254c0e278
		'''
		if self.user.level_obj == levels.Novice:
			days = self._get_novice_days()
		elif self.user.level_obj == levels.Beginner:
			days = self._get_beginner_days()
		elif self.user.level_obj == levels.Intermediate:
			days = self._get_intermediate_days()
<<<<<<< HEAD
=======

>>>>>>> 1f1a621578ff8fcfdd7ede4cfcc91f9254c0e278
		cardio_days , rt_days = self._get_days_distribution(days)
		return namedDays(cardio_days , rt_days , days.total)
