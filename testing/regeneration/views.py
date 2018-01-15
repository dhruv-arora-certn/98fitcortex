from django.shortcuts import render
from django.db.models import Q

from rest_framework import generics

from .models import RegenerationLog


# Create your views here.
class RegenerableView(generics.GenericAPIView):

	def get_object_hook(self):
		raise NotImplementedError("The child class should implement this function")

	def get_regenerate_log_filter(self):
		raise NotImplementedError("The child class should implement this function")

	def get_regeneration_log_object(self):
		filter_ = Q(**self.get_regenerate_log_filter())

		try:
			regen_obj = RegenerationLog.objects.get(filter_)
		except RegenerationLog.DoesNotExist:
			regen_obj = None

		return regen_obj

	def get_object(self):
		regen_obj = self.get_regeneration_log_object()
		obj = self.get_object_hook()

		if regen_obj:
			return self.regeneration_hook(obj)

		#No Regeneration is required so just return the obj
		return obj

		if regen_obj:
			return {
				"status" : True,
				"obj" : str(obj_to_regenerate)
			}
		return {
			"status" : False
		}


class TestRegenerableView(RegenerableView):

	type = "diet"

	def get_object_hook(self):
		return model.objects.last()

	def get_regenerate_log_filter(self):
		'''
		Customer , Year , Week , Type , regenerated
		'''
		return  Q(customer = customer) & Q(year = year) & Q(week = week) & Q(type = self.diet) & Q(regenerated = False)
