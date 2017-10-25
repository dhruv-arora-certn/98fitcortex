import random
import operator
import itertools
import enum
import collections

from workout import models
from workoutplan import exercise
from .utils import Luggage , CardioStretchingFilter

from django.core.cache import cache
from django.db.models import Q

class Base():

	def __init__(self):
		pass

class Warmup(Base):
	_type = "warmup"
	duration = 300

	def __init__(self , user , mainCardio = None , bodyPartInFocus = Q()):
		self.user = user
		self.mainCardio = mainCardio
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
		print("Warmup ",self.mainCardio.cardioType)
		if self.mainCardio.cardioType== exercise.FloorBasedCardio:
			print("Warmup Floor Based")
			return self.floor_based_cardio()
		elif self.mainCardio.cardioType == exercise.TimeBasedCardio:
			print("Warmup Time Based")
			return self.time_based_cardio()

	def floor_based_cardio(self):
		'''
		To be used in the case where main exercise is Floor Based Cardio
		'''
		return self.normal_warmup_cooldown()

	def normal_warmup_cooldown(self):
		'''
		To be used in the case where a normal Warm Up and Cool Down is to be generated
		'''
		filters = self.get_intensity_filter()
		modelToUse = models.WarmupCoolDownTimeBasedExercise
		l = []

		for e in self.get_intensity_filter():
			print(e.get('filter') & self.bodyPartInFocus)
			warmup = exercise.Warmup(
				self.user,
				duration = e.get('duration'),
				modelToUse = modelToUse,
				filterToUse = e.get('filter') & self.bodyPartInFocus
			).build()
			l.extend(warmup.selected)
		return  l

	def time_based_cardio(self):
		class Warmup:
			duration = 300
			def __str__(self):
				return self.workout_name
			def __repr__(self):
				return self.workout_name
			def __init__(self,name):
				self.workout_name = name

		return list(map(lambda x : Warmup(x) , [
			e.functional_warmup for e in self.mainCardio.cardio
		]))

	def build(self):
		self.selected = {
			"warmup" : self.decideWarmup()
		}
		return self

	def as_dict(self):
		return {
			"warmup" : self.selected
		}


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
		self.selected = {
			"cardio" : self.cardio ,
			"resistancetraining" : self.rt
		}
		return self

	def as_dict(self):
		return {
			"cardio" : self.cardio,
			"resistance_training" : self.rt
		}


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
		#return CardioStretchingFilter
		l = []
		for e in CardioStretchingFilter:
			stretching = exercise.Stretching(
				user = self.user,
				filterToUse = e.value.filter
			)
			stretching.build()
			print(l)
			l.extend(stretching.selected)
		return l


	def build(self):
		l = {"stretching" : []}
		if self.resistance_filter:
			self.rt_stretching = self.build_rt()
			l['stretching'].extend(self.rt_stretching)

		if self.cardio:
			self.cardio_stretching = self.build_cardio()
			l['stretching'].extend(self.cardio_stretching)
		self.selected = l
		return self
