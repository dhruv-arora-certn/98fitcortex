import random
import operator

from workout import models
from workoutplan import exercise
from .utils import Luggage
from .resistance_data import UpperBodyIdentifier , LowerBodyIdentifier

from django.core.cache import cache
from django.db.models import Q

class Base():

	def __init__(self):
		pass

class Warmup(Base):
	_type = "warmup"
	duration = 300

	def __init__(self , user , mainExercise = None):
		self.user = user
		self.mainExercise = mainExercise

	def get_body_part_filter(self):
		if isinstance(self.mainExercise.conditionalType , exercise.ResistanceTraining):
			return Q()


	def get_intensity_filter(self):
		if self.user.is_novice():
			return [{
				"filter" : Q(exercise_level = "Low"),
				"duration" : 300
			}]
		elif self.user.is_intermediate():
			return [
				{
					"filter" : Q(exercise_level = "Low"),
					"duration" : 150
				},
				{
					"filter" : Q(exercise_level = "Moderate"),
					"duration" : 150
				}
			]
		elif self.user.is_intermediate():
			return [
				{
					"filter" : Q(exercise_level = "Low"),
					"duration" : 60 
				},
				{
					"filter" : Q(exercise_level = "Moderate"),
					"duration" : 60
				},
				{
					"filter" : Q(exercise_level = "High"),
					"duration" : 180
				}
			]
	def decideWarmup(self):
		'''
		Decide Which Function is to be called For generating the Warmup
		The function is assigned to the object rather than returned,
		Self is returned instead
		This will enable me to perform chaining and allow subsequent functions to use the attribute
		'''
		if isinstance(self.mainExercise.cardioType, exercise.FloorBasedCardio):
			self.__funcToCall = self.floor_based_cardio
		return self

	def floor_based_cardio(self):
		'''
		To be used in the case where main exercise is Floor Based Cardio
		'''
		self.normal_warmup_cooldown()

	def normal_warmup_cooldown(self):
		'''
		To be used in the case where a normal Warm Up and Cool Down is to be generated
		'''
		filters = self.get_intensity_filter()
		modelToUse = models.WarmupCoolDownTimeBasedExercise
		l = []

		for e in self.get_intensity_filter():
			warmup = exercise.Warmup(
				self.user,
				duration = e.get('duration'),
				modelToUse = modelToUse,
				filterToUse = e.get('filter') & self.get_body_part_filter()
			).build()
			l.extend(*warmup.selected)

		return  l

	def time_based_cardio(self):
		pass


class Main(Base):
	_type = "main"

	def __init__(self , user , cardioType = random.choice([exercise.FloorBasedCardio , exercise.TimeBasedCardio]) ):
		self.user = user
		self.cardioType = cardioType

	def buildCardio(self):
		duration = 900
		cardio = self.cardioType(
			self.user,
			duration
		)
		cardio.build()
		return cardio.selected

	def buildResistanceTraining(self):
		self.conditionalType = exercise.ResistanceTraining
		pass

	def buildCoreStrengthening(self):
		self.duration = 300
		self.conditionalType = exercise.CoreStrengthening
		core = exercise.CoreStrengthening(
			user = self.user,
			duration = self.duration,
		)
		core.build()
		return core.selected

	def buildRT(self):
		if self.user.is_novice():
			return self.buildCoreStrengthening()
		return self.buildResistanceTraining()

	def build(self):
		'''
		Build exercises after assembly
		'''
		self.cardio = self.buildCardio()
		self.rt = self.buildRT()


class CoolDown(Base):
	_type = "cooldown"
	def __init__(self):
		pass

class Stretching(Base):
	_type = "stretching"
	def __init__(self):
		pass
