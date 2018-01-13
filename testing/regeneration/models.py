from django.db import models

from epilogue.models import Customer

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
	customer = models.ForeignKey(Customer , related_name = "regeneration_nodes" , on_delete = models.CASCADE , null = True)
	created = models.DateTimeField(auto_now_add = True)
	regenerated_on = models.DateTimeField(auto_now = True)
	regenerated = models.BooleanField(default = False)

	def toggleStatus(self):
		self.regenerated = not self.regenerated
		self.save()
		return self


	def __str__(self):
		return "%s:%s:(%s,%s)"%(
			self.type,
			self.customer,
			self.year,
			self.week
		)

	class Meta:
		unique_together = ("customer" , "year" , "week" , "type")
		index_together = ("customer" , "year" , "week" , "type")

