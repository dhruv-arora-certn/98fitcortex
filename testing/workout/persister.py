import itertools
import functools
import logging

from epilogue.utils import get_week , get_day , get_year

from workout import models

logger = logging.getLogger(__name__)

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
            "customer_id" : self.workout.user.id,
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

    def __str__(self):
        return "Day:%d"%self.day
    def __repr__(self):
        return "Day:%d"%self.day.day

    def persist_exercise(self, exercise , mod = None):
        e = ExercisePersister(
            exercise,
            day = self.day.day,
            workout = self.workout,
            mod = mod
        )
        return e.persist()

    def forward(self):

        self.exercises = {}
        for i,e in self.day.iterexercises():
            if not self.exercises.get(i):
                self.exercises[i] = []
            print("Exercises",e)
            exercises = map(
                functools.partial(self.persist_exercise , mod = i),
                e
            )
            self.exercises[i].extend([o for o in exercises])
        return self

    def persist(self):
        try:
            self.forward()
        except:
            [
                e.model_obj.delete() for e in itertools.chain(*self.exercises.values())
            ]
            raise
        return self

class ExercisePersister:

    model = models.GeneratedExercisePlanDetails

    def __init__(self, exercise , day = None , workout = None, mod = None):
        self.exercise = exercise
        self.workout = workout
        self.day = day

        if not mod:
            mod = self.exercise.module_name

        self.mod = mod

    def __repr__(self):
        return "%s : %s : Persister"%(self.exercise.workout_name , self.mod)

    def get_fields(self):
        return {
            "workoutplan" : self.workout,
            "day" : self.day,
            "workout_name" : self.exercise.workout_name,
            "time" : self.get_time(self.exercise),
            "reps" : self.get_reps(self.exercise),
            "sets" : self.get_sets(self.exercise),
            "machine_name" : self.get_equipment(self.exercise),
            "equipment_name" : self.get_equipment(self.exercise),
            "mod_name" : self.mod,
            "mod_id" : self.exercise.id,
            "description" : self.get_description(self.exercise),
            "exercise_level" : self.get_exercise_level(self.exercise),
            "exercise_type" : 0,
            "muscle_group" : self.get_muscle_group(self.exercise),
            "image" : self.get_image(self.exercise)
        }

    def persist(self , save = True):
        if save:
            self.model_obj = self.model.objects.create(
                **self.get_fields()
            )
        else:
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
        return  getattr(obj , "sets" , 1)

    def get_reps(self , obj):
        return  str(getattr(obj , "reps" , 1))

    def get_muscle_group(self , obj):
        return getattr(obj , "muscle_group_name" , "")

    def get_equipment(self ,obj):
        equipment = getattr(obj , "machine_name" , None)
        if isinstance(equipment , str) and equipment.lower().strip() == "na":
            return ""
        return equipment

    def get_description(self ,obj):
        description = getattr(obj , "description" , "")
        if description and description.lower().strip() == "na":
            return ""
        return description

    def get_exercise_type(self , obj):
        return getattr(obj , "exercise_type" , "")

    def get_body_part(self , obj):
        return getattr(obj , "body_part" , None)

    def get_exercise_level(self , obj):
        return getattr(obj , "exercise_level" , "")

    def get_time(self , obj):
        return getattr(obj , "duration" , 0)

    def __str__(self):
        return self.exercise.workout_name
