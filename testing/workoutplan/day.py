from . import exercise_type
from . import exercise
from . import shared_globals

from django.db.models import Q
from .utils import DummyCoolDown

class ExerciseDay:

	def __init__(self , day , user ,make_cardio = False , resistance_filter = Q()):
		self.day = day
		self.make_cardio = make_cardio
		self.make_rt = bool(resistance_filter)
		self.resistance_filter = resistance_filter
		self.user = user

	def __str__(self):
		return "Day %s"%self.day

	def __repr__(self):
		return self.__str__()

	def generate(self):
		self.buildMain(self)

	def buildMain(self):
		self.main = exercise_type.Main(self.user ,resistance_filter =  self.resistance_filter)
		self.main.build()

	def buildWarmup(self):
		self.warmup = exercise_type.Warmup(self.user , mainCardio = self.main )
		self.warmup.build()
		return self

	def buildCoolDown(self):
		self.cooldown = exercise_type.Warmup(self.user , mainCardio = self.main)
		self.cooldown.build()
		self.cooldown.selected['cooldown'] = self.cooldown.selected['warmup']
		del self.cooldown.selected['warmup']
		if self.resistance_filter:
			self.cooldown.selected['cooldown'].append(
				DummyCoolDown(900 , "Slow Walk")
			)
		return self

	def buildStretching(self):

		class Stretching:
			selected = {"stretching" : []}

		self.stretching = Stretching()

		if self.resistance_filter:
			self.rt_stretching = exercise_type.Stretching( self.user , resistance_filter = self.resistance_filter)
			self.rt_stretching.build()
			self.stretching.selected.get('stretching').extend(self.rt_stretching.selected.get("stretching"))

		if self.make_cardio:
			self.cardio_stretching = exercise_type.Stretching(self.user , cardio = True)
			self.cardio_stretching.build()
			self.stretching.selected.get('stretching').extend(self.cardio_stretching.selected.get("stretching"))

	def get_main_cardio(self):
		return self.main.cardio

	def build(self):
		shared_globals.day_in_progress = self.day
		self.buildMain()
		self.buildWarmup()
		self.buildStretching()
		self.buildCoolDown()
		return self

	def save(self):
		'''
		Persist the workout of the user to database;
		Use workout.models.ExercisePlanDetail;
		
		'''
		return

	def serialize(self):
		return {
			**self.warmup.selected,
			**self.main.selected,
			**self.stretching.selected
		}
