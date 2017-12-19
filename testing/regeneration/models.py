from django.db import models

# Create your models here.
from .receivers import *



class RegenerationLog(models.Model):
	DIET = 'diet'
	WORKOUT = 'workout'
	TYPE_CHOICES = (
		(DIET , 'Diet'),
		(WORKOUT , 'Workout')
	)
	year = models.IntegerField()
	week = models.IntegerField()
	type = models.CharField(
		max_length = 7,
		choices = TYPE_CHOICES
	)
	created = models.DateTimeField(auto_now_add = True)
	regenerated = models.DateTimeField(auto_now = True)
