#Contains Exercise Tables

from django.db import models
from epilogue.models import *

# Create your models here.

class CardioFloor(models.Model):
	workout_name = models.CharField(max_length=250, blank=True, null=True)
	reps = models.IntegerField(blank=True, null=True)
	duration = models.CharField(max_length=100, blank=True, null=True)
	swing1 = models.CharField(max_length=10, blank=True, null=True)
	home = models.CharField(max_length=10, blank=True, null=True)
	gym = models.CharField(max_length=10, blank=True, null=True)
	machine_required = models.CharField(max_length=10, blank=True, null=True)
	machine_name = models.CharField(max_length=250, blank=True, null=True)
	exercise_level = models.CharField(max_length=50, blank=True, null=True)
	description = models.CharField(max_length=255, blank=True, null=True)
	status = models.IntegerField(blank=True, null=True)
	image_name = models.CharField(max_length=250, blank=True, null=True)
	#swing_field = models.BooleanField()
	#home_field = models.BooleanField()
	#gym_field = models.BooleanField()

class CardioTimeBased(models.Model):
	workout_name = models.CharField(max_length=250, blank=True, null=True)
	duration = models.CharField(max_length=250, blank=True, null=True)
	home = models.CharField(max_length=10, blank=True, null=True)
	gym = models.CharField(max_length=10, blank=True, null=True)
	machine_required = models.CharField(max_length=10, blank=True, null=True)
	machine_required_home = models.CharField(max_length=250, blank=True, null=True)
	machine_required_gym = models.CharField(max_length=250, blank=True, null=True)
	exercise_level = models.CharField(max_length=50, blank=True, null=True)
	functional_warmup = models.CharField(max_length=200, blank=True, null=True)
	status = models.IntegerField(blank=True, null=True)
	image_name = models.CharField(max_length=100, blank=True, null=True)

class NoviceCoreStrengthining(models.Model):
	workout_name = models.CharField(max_length=250)
	reps = models.CharField(max_length=50)
	duration = models.CharField(max_length=10)
	hold = models.CharField(max_length=10)
	swing1 = models.CharField(max_length=10)
	rotation = models.CharField(max_length=10)
	swing2 = models.CharField(max_length=10)
	sets = models.IntegerField()
	home = models.CharField(max_length=50)
	gym = models.CharField(max_length=50)
	machine_required = models.CharField(max_length=10)
	machine_name = models.CharField(max_length=100, blank=True, null=True)
	exercise_level = models.CharField(max_length=100, blank=True, null=True)
	muscle_group_cat = models.CharField(max_length=100, blank=True, null=True)
	muscle_group_name = models.CharField(max_length=100, blank=True, null=True)
	body_part = models.CharField(max_length=100, blank=True, null=True)
	description = models.CharField(max_length=255, blank=True, null=True)
	status = models.IntegerField(blank=True, null=True)
	image_name = models.CharField(max_length=200, blank=True, null=True)
