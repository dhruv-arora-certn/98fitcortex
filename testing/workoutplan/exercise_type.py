import random
import operator
import itertools
import enum
import collections

from workout import models
from workoutplan import exercise
from .utils import Luggage

from django.core.cache import cache
from django.db.models import Q

class Base():

	def __init__(self):
		pass

class Warmup(Base):
	_type = "warmup"
	duration = 300

	def __init__(self , user , mainCardioType = None , bodyPartInFocus = Q()):
		self.user = user
		self.mainCardioType = mainCardioType
		self.bodyPartInFocus = bodyPartInFocus
		self.selected = []

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
		if isinstance(self.mainCardioType, exercise.FloorBasedCardio):
			return self.floor_based_cardio
		elif isinstance(self.mainCardioType , exercise.TimeBasedCardio):
			return self.time_based_cardio

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
				filterToUse = e.get('filter') & self.bodyPartInFocus
			).build()
			l.extend(*warmup.selected)


		return  l

	def time_based_cardio(self):
		pass

	def build(self):
		self.selected = self.normal_warmup_cooldown()
		return self


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

	@property
	def selected(self):
		return itertools.chain([self.cardio] ,  self.rt)


class CoolDown(Base):
	_type = "cooldown"
	def __init__(self):
		pass

class Stretching(Base):
	_type = "stretching"
	def __init__(self , user , resistance_filter = None , cardio = False):
		self.user = user
		self.resistance_filter = resistance_filter
		self.cardio = cardio

	def build_rt(self):
		l = []
		for e in self.resistance_filter.filters:
			stretching = exercise.Stretching(
				user = self.user,
				filterToUse = e.get('filter') 
			)
			stretching.build()
			l.extend(stretching.selected)
		return l

	def build_cardio(self):
		filter_tuple = collections.namedtuple("filter_" , ["filter" , "count"])

		class CardioStretchingFilter(enum.Enum):
			QUADS = filter_tuple(
				filter = Q(muscle_group_name = "Quadriceps"),
				count = 1
			)
			CHEST = filter_tuple(
				filter = Q(muscle_group_name  = "Chest"),
				count = 1
			)
			GLUTES = filter_tuple(
				filter = Q(muscle_group_name = "Glutes"),
				count = 1
			)
			BACK = filter_tuple(
				filter = Q(muscle_group_name = "Back"),
				count = 1
			)
		#return CardioStretchingFilter
		for e in CardioStretchingFilter:
			l = []
			stretching = exercise.Stretching(
				user = self.user,
				filterToUse = e.value.filter
			)
			stretching.build()
			print(l)
			l.extend(stretching.selected)
		return l


	def build(self):
		if self.resistance_filter:
			self.rt_stretching = self.build_rt()

		if self.cardio:
			self.cardio_stretching = self.build_cardio()


