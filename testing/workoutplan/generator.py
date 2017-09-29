from . import levels
from .goals import Goals
from .utils import NoviceDays , BeginnerDays , IntermediateDays
import random

class Generator():

	def __init__(self, user):
		self.user =  user 

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

		cardio = random.sample(
			[1,2,3,4,5,6,7],
			days.cardio
		)
		return cardio
