from . import exercise_type
from . import exercise
from django.db.models import Q

class ExerciseDay:

	def __init__(self , day , user ,make_cardio = False , resistance_filter = Q()):
		self.day = day
		self.make_cardio = make_cardio
		self.resistance_filter = resistance_filter
		self.user = user

	def __str__(self):
		return "Day %s"%self.day

	def __repr__(self):
		return self.__str__()

	def generate(self):
		self.buildMain(self)

	def buildMain(self):
		self.main = exercise_type.Main(self.user)
		self.main.build()

	def buildWarmup(self):
		if self.main.cardioType == exercise.TimeBasedCardio:
			self.warmup = [e.functional_warmup for e in self.main.cardio]
			return 
		self.warmup = exercise_type.Warmup(self.user , mainCardioType = self.get_main_cardio())
		self.warmup.build()

	def buildStretching(self):
		if self.resistance_filter:
			self.rt_stretching = exercise_type.Stretching( self.user , resistance_filter = self.resistance_filter)
			self.rt_stretching.build()

		if self.make_cardio:
			self.cardio_stretching = exercise_type.Stretching(self.user , cardio = True)
			self.cardio_stretching.build()

	def get_main_cardio(self):
		return self.main.cardio

	def build(self):
		self.buildMain()
		self.buildWarmup()
		self.buildStretching()
		return self
