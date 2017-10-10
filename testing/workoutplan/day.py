from . import exercise_type
from django.db.models import Q

class ExerciseDay:

	def __init__(self , day , user ,make_cardio = False , resistance_filter = Q()):
		self.day = day
		self.make_cardio = False
		self.resistance_filter = resistance_filter
		self.user = user

	def __str__(self):
		return "Day %s"%self.day

	def __repr__(self):
		return self.__str__()

	def generate(self):
		self.buildMain(self)

	def buildMain(self):
		self.main = exercise_type.Main(
