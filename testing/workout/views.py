from django.shortcuts import render
from django.core.cache import cache

# Create your views here.
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response

from epilogue.authentication import CustomerAuthentication
from epilogue.utils import get_week , get_day

from workout.models import *
from workout.serializers import *
from workout.utils import get_day_from_generator

from workoutplan.generator import Generator

import random
import json
import logging

def shuffle(qs):
	l = list(qs)
	random.shuffle(l)
	return l[:5]

class WarmupView(generics.ListAPIView):
	authentication_classes  = [CustomerAuthentication]
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = WarmupSerializer

	def get_queryset(self):
		return shuffle(WarmupCoolDownMobilityDrillExercise.objects.all())

class CardioView(generics.ListAPIView):
	authentication_classes  = [CustomerAuthentication]
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = CardioTimeBasedSerializer

	def get_queryset(self):
		return shuffle(CardioTimeBasedExercise.objects.all())

class NoviceCoreView(generics.ListAPIView):
	authentication_classes  = [CustomerAuthentication]
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = NoviceCoreStrengthiningExerciseSerializer

	def get_queryset(self):
		return shuffle(NoviceCoreStrengthiningExercise.objects.all())

class StretchingView(generics.ListAPIView):
	authentication_classes  = [CustomerAuthentication]
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = StretchingExerciseSerializer

	def get_queryset(self):
		return shuffle(StretchingExercise.objects.all())

class CoolDownView(generics.ListAPIView):
	authentication_classes  = [CustomerAuthentication]
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = CoolDownSerializer

	def get_queryset(self):
		return shuffle(WarmupCoolDownMobilityDrillExercise.objects.all())

class WorkoutView(generics.GenericAPIView):
	serializer_class = WorkoutSerializer
	authentication_classes = [CustomerAuthentication]
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		week_id = self.kwargs('week_id' , get_week())
		day = self.kwargs('day',get_day() )

	def get_warmup(self , gen):
		warmup = get_day_from_generator(gen , self.kwargs.get('day',1)).warmup.selected['warmup']
		warmup_s = ExerciseSerialzier(warmup , many = True)
		return {
			"warmup" : warmup_s.data
		}

	def get_main(self,gen):
		main = get_day_from_generator(gen , self.kwargs.get('day',1)).main.selected
		c = ExerciseSerialzier(main['cardio'], many = True)
		data = {
			"cardio" : c.data
		}
		if main.get('resistance_training'):
			rt = ExerciseSerialzier(main.get('resistance_training') , many = True)
			rt_key = "resistance_training"
			data.update({
				rt_key : rt.data
			})
		elif main.get('core_strengthening'):
			rt = ExerciseSerialzier(main.get('core_strengthening') , many = True)
			rt_key = "core_strengthening"
			data.update({
				rt_key : rt.data
			})
		return data

	def get_stretching(self,gen):
		s = get_day_from_generator(gen , self.kwargs.get('day',1)).stretching.selected
		sw = ExerciseSerialzier(s['stretching'] , many = True)
		return {
			"stretching" : sw.data
		}

	def get_cooldown(self , gen):
		cooldown = get_day_from_generator(gen , self.kwargs.get('day',1)).cooldown.selected['cooldown']
		cooldown_serializer = ExerciseSerialzier(cooldown , many = True)
		return {
			"cooldown": cooldown_serializer.data
		}

	def get_object(self):
		key = "workout_%d_%s"%(self.request.user.id , self.kwargs['week_id'])
		cached_data = cache.get(key)
		logger = logging.getLogger(__name__)
		print(logger.name)
		if cached_data:
			logger.debug("Returning Workout from cache")
			logger.debug(cached_data.get(self.kwargs['day']))
			return cached_data.get(int(self.kwargs['day']))
		else:
			logger.debug("Generating Workout")
			gen = Generator(self.request.user)
			gen.generate()
			weekly_data = gen.weekly_as_dict()
			cache.set(key , weekly_data)
			return weekly_data[int(self.kwargs['day'])]

	def get(self , request , *args , **kwargs):
		data = self.get_object()
		print(data)
		serialized_data = {}
		for k,v in data.items():
			serialized_data[k] = ExerciseSerialzier(
				v , many = True
			).data
		return Response(
			serialized_data
		)
