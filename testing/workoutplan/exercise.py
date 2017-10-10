import random

from django.core.cache import cache
from django.db.models import Q
from workout import models
from workoutplan.utils import Luggage

class ExerciseBase:

	def __init__(self , user , duration):
		self.user = user
		self.duration = duration
		self.cache_key = self.__class__.__name__
		self.selected = []

	def build(self):
		items = self.get_items()
		l = Luggage(
			self.duration,
			items,
			"duration"
		).pickAndPack()
		self.selected.append(l.packed)
		return self

	def get_items(self):
		return list(cache.get_or_set(self.cache_key , self.model.objects.all()))

class FloorBasedCardio(ExerciseBase):
	def __init__(self , user , duration):
		super().__init__(user , duration)
		self.model = models.CardioFloorExercise


class TimeBasedCardio(ExerciseBase):

	def __init__(self , user , duration):
		super().__init__( user , duration )
		self.model = models.CardioTimeBasedExercise

	def build(self):
		self.selected = random.choice(self.get_items())
		return self

class ResistanceTraining(ExerciseBase):

	def __init__( self , user , duration , filters):
		super().__init__( user , duration)
		self.filters = filters
		self.model = models.ResistanceTrainingExercise


class CoreStrengthening(ExerciseBase):

	def __init__(self , user , duration = 0, **kwargs):
		super().__init__(user , duration)
		self.model = models.NoviceCoreStrengthiningExercise

class Warmup(ExerciseBase):

	def __init__(self , user , duration = 300 , modelToUse = None , filterToUse = Q() ,**kwargs):
		assert modelToUse , "Model Should be defined"
		super().__init__(user , duration)
		self.model = modelToUse
		self.filter = filterToUse
		self.cache_key = "%s_%s"%(self.model.__name__ , str(filterToUse))

	def get_items(self):
		a =  cache.get_or_set(self.cache_key , list(self.model.objects.filter(self.filter)))
		return a
