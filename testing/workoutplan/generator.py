from . import levels
from .goals import Goals
from .utils import NoviceDays , BeginnerDays , IntermediateDays , days as namedDays
import random

class Generator():

	def __init__(self, user):
		self.user =  user 
<<<<<<< HEAD
		self.conditional_days = self.get_conditional_days()
=======
>>>>>>> 44e56182666838d67e55723fda63e47c251764cc

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
