#Contains Exercise Tables

from django.db import models
from epilogue.models import *  

# Create your models here.

class BaseExercise():

	def __repr__(self):
		return "%s : %s"%(str(self.workout_name) , getattr(self  , "exercise_level" , "None"))

	def __str__(self):
		return self.workout_name

class CardioFloorExercise(BaseExercise,models.Model):
	workout_name = models.CharField(max_length=250, blank=True, null=True)
	reps = models.IntegerField(blank=True, null=True)
	duration = models.IntegerField(max_length=100, blank=True, null=True)
	swing1 = models.BooleanField(default = True)
	home = models.BooleanField(default = True)
	gym = models.BooleanField(default = True)
	machine_required = models.BooleanField(default = True)
	machine_name = models.CharField(max_length=250, blank=True, null=True)
	exercise_level = models.CharField(max_length=50, blank=True, null=True)
	description = models.CharField(max_length=255, blank=True, null=True)
	status = models.IntegerField(blank=True, null=True)
	image_name = models.CharField(max_length=250, blank=True, null=True)
	
class CardioTimeBasedExercise(BaseExercise,models.Model):
	workout_name = models.CharField(max_length=250, blank=True, null=True)
	duration = models.CharField(max_length=250, blank=True, null=True)
	home = models.BooleanField(default = True)
	gym = models.BooleanField(default = True)
	machine_required = models.BooleanField(default = True)
	machine_required_home = models.CharField(max_length=250, blank=True, null=True)
	machine_required_gym = models.CharField(max_length=250, blank=True, null=True)
	exercise_level = models.CharField(max_length=50, blank=True, null=True)
	functional_warmup = models.CharField(max_length=200, blank=True, null=True)
	status = models.IntegerField(blank=True,default = 1)
	image_name = models.CharField(max_length=100, blank=True, null=True)

class NoviceCoreStrengthiningExercise(BaseExercise,models.Model):
	workout_name = models.CharField(max_length=250)
	reps = models.CharField(max_length=50)
	duration = models.IntegerField()
	hold = models.BooleanField(default = False)
	swing1 = models.BooleanField(default = False)
	rotation = models.BooleanField()
	swing2 = models.BooleanField(default = False)
	sets = models.IntegerField()
	home = models.BooleanField(default = True)
	gym = models.BooleanField(default = True)
	machine_required = models.BooleanField(default = True)
	machine_name = models.CharField(max_length=100, blank=True, null=True)
	exercise_level = models.CharField(max_length=100, blank=True, null=True)
	muscle_group_cat = models.CharField(max_length=100, blank=True, null=True)
	muscle_group_name = models.CharField(max_length=100, blank=True, null=True)
	body_part = models.CharField(max_length=100, blank=True, null=True)
	description = models.CharField(max_length=255, blank=True, null=True)
	status = models.IntegerField(blank=True, null=True)
	image_name = models.CharField(max_length=200, blank=True, null=True)

class ResistanceTrainingExercise(BaseExercise,models.Model):
	workout_name = models.CharField(max_length = 100,blank=True, null=True)
	exercise_group = models.CharField(max_length = 30,blank=True, null=True)
	left_right = models.BooleanField(default = True)
	home = models.BooleanField(default = True)
	gym = models.BooleanField(default = True)
	eqip_name_home = models.CharField(max_length = 100,blank=True, null=True)
	machine_required = models.BooleanField(default = True)
	machine_name = models.CharField(max_length = 100,blank=True, null=True)
	exercise_level = models.CharField(max_length  =10,blank=True, null=True)
	muscle_group_cat = models.CharField(max_length = 100,blank=True, null=True)
	muscle_group_name = models.CharField(max_length = 100,blank=True, null=True)
	sub_muscle_group = models.CharField(max_length = 30,blank=True, null=True)
	body_part = models.CharField(max_length = 30,blank=True, null=True)
	exercise_type = models.CharField(max_length = 100,blank=True, null=True)
	status = models.IntegerField(default = 1)
	image_name = models.CharField(max_length = 50,blank=True, null=True)


class StretchingExercise(BaseExercise,models.Model):
	workout_name = models.CharField(max_length=250, blank=True, null=True)
	swing1 = models.BooleanField(default = True)
	home = models.BooleanField(default = True)
	gym = models.BooleanField(default = True)
	machine_required = models.BooleanField(default = True)
	machine_name = models.CharField(max_length=250, blank=True, null=True)
	muscle_group_cat = models.CharField(max_length=250, blank=True, null=True)
	sub_muscle_group_name = models.CharField(max_length=250, blank=True, null=True)
	muscle_group_name = models.CharField(max_length=250, blank=True, null=True)
	body_part = models.CharField(max_length=250, blank=True, null=True)
	description = models.CharField(max_length=255, blank=True, null=True)
	status = models.IntegerField(blank=True, null=True)
	image_name = models.CharField(max_length=250, blank=True, null=True)


class WarmupCoolDownMobilityDrillExercise(BaseExercise,models.Model):
	workout_name = models.CharField(max_length = 100)
	duration = models.IntegerField(default = 0)
	reps = models.IntegerField(default = 0)
	swing1 = models.BooleanField(default = False)
	rotation = models.BooleanField(default = False)
	swing2 = models.BooleanField(default = False)
	home  = models.BooleanField(default = True)
	gym  = models.BooleanField(default = True)
	machine_required  = models.BooleanField(default = True)
	machine_name = models.CharField(max_length = 100, blank=True, null=True)
	exercise_level = models.CharField(max_length = 30, blank=True, null=True)
	joint_name = models.CharField(max_length = 50, blank=True, null=True)
	body_part = models.CharField(max_length = 50, blank=True, null=True)
	muscle_group_name = models.CharField(max_length = 100, blank=True, null=True)
	description = models.CharField(max_length = 255, blank=True, null=True)
	status = models.IntegerField(default = 0)
	image_name = models.CharField(max_length = 50, blank=True, null=True)


class WarmupCoolDownTimeBasedExercise(BaseExercise,models.Model):	
	workout_name = models.CharField(max_length = 100)
	duration = models.IntegerField()
	total_time = models.IntegerField()
	time_unit = models.CharField(max_length = 10 , default = "secs")
	machine_required  = models.BooleanField()
	machine_name = models.CharField(max_length = 100)
	exercise_level = models.CharField(max_length = 30)
	muscle_group = models.CharField(max_length = 50)
	body_part = models.CharField(max_length = 50)
	status = models.IntegerField()
	home  = models.BooleanField()
	gym  = models.BooleanField()
