from .exercise_type import ResistanceTrainingExercise
from django.db.models import Q

class ExerciseDay:

	def __init__(self , day , resistance_filter = Q()):
		self.day = day

	def __str__(self):
		return "Day %s"%self.day

	def __repr__(self):
		return self.__str__()

