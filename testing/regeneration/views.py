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
		regen_obj = RegenerationLog.objects.get(filter_)

		if regen_obj:
			return {
				"status" : True
			}
		return {
			"status" : False
		}

	def get_object(self):
		regen_obj = self.get_regeneration_log_object()

		if regen_obj:
			return {
				"status" : True
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
