import itertools

from epilogue.utils import get_week , get_day , get_year

from workout import models


class PersisterBase:

	def save(self):
		pass

class WorkoutWeekPersister:

	model = models.GeneratedExercisePlan

	def __init__(self , workout , week = None):

		if not week:
			week = get_week()

		self.week = week
		self.workout = workout

	def get_fields(self):
		return {
			"year" : get_year(),
			"week_id" : self.week,
			"user_week_id" : self.workout.user.user_relative_workout_week,
			"customer" : self.workout.user,
		}

	def forward(self):
		self.days = []
		for e in self.workout.iterdays():
			day = WorkoutDayPersister(e , self.model_obj)
			day.persist()
			self.days.append(day)
		return self

	def persist(self):
		self.model_obj = self.model.objects.create(
			**self.get_fields()
		)
		try:
			self.forward()
		except :
			self.model_obj.delete()
			raise
		return self

class WorkoutDayPersister:

	model = models.GeneratedExercisePlanDetails

	def __init__(self , day , workout):
		self.day = day
		self.workout = workout

	def persist_exercise(self, exercise):
		e = ExercisePersister(
			exercise,
			day = self.day.day,
			workout = self.workout
		)
		return e.persist()

	def forward(self):

		self.exercises = {}
		for i,e in self.day.iterexercises():
			if not self.exercises.get(i):
				self.exercises[i] = []
			print("Exercises",e)
			exercises = map(
				self.persist_exercise,
				e
			)
			self.exercises[i].extend([o for o in exercises])
		return self

	def persist(self):
		try:
			self.forward()
		except:
			[
				e.delete() for e in itertools.chain(*self.exercises.values())
			]
			raise
		return self

class ExercisePersister:

	model = models.GeneratedExercisePlanDetails

	def __init__(self, exercise , day = None , workout = None):
		self.exercise = exercise
		self.workout = workout
		self.day = day

	def get_fields(self):
		return {
			"workoutplan" : self.workout,
			"day" : self.day,
			"workout_name" : self.exercise.workout_name,
			"time" : self.exercise.duration,
			"reps" : self.get_reps(self.exercise),
			"sets" : self.get_sets(self.exercise),
			"machine_name" : self.get_equipment(self.exercise),
			"equipment_name" : self.get_equipment(self.exercise),
			"mod_name" : self.exercise.module_name,
			"mod_id" : self.exercise.id
		}

	def persist(self):
		self.model_obj = self.model(
			**self.get_fields()
		)
		return self

	def get_image(self , obj):
		base = "https://s3-ap-southeast-1.amazonaws.com/98fitasset/image/exercise/"
		if hasattr(obj , "image_name") and getattr(obj , "image_name"):
			return "%s%s"%(base,getattr(obj , "image_name" , "http:/www.98fit.com//webroot/workout_images/workout_blank.jpg"))
		return "http://www.98fit.com/webroot/workout_images/workout_blank.jpg"

	def get_sets(self , obj):
		return  getattr(obj , "sets" , None)

	def get_reps(self , obj):
		return  getattr(obj , "reps" , None)

	def get_muscle_group(self , obj):
		return getattr(obj , "muscle_group_name" , None)

	def get_equipment(self ,obj):
		equipment = getattr(obj , "machine_name" , None)
		if isinstance(equipment , str) and equipment.lower().strip() == "na":
			return None
		return equipment
