from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response

from epilogue.authentication import CustomerAuthentication
from epilogue.utils import get_week , get_day

from workout.models import *
from workout.serializers import *

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
		warmup = gen.D1.warmup.selected['warmup']
		warmup_s = ExerciseSerialzier(warmup , many = True)
		return {
			"warmup" : warmup_s.data
		}

	def get_main(self,gen):
		main = gen.D1.main.selected
		c = ExerciseSerialzier(main['cardio'], many = True)
		rt = ExerciseSerialzier(main['resistancetraining'] , many = True)
		return {
			"cardio" : c.data,
			"resistance_training" : rt.data
		}

	def get_stretching(self,gen):
		s = gen.D1.stretching.selected
		sw = ExerciseSerialzier(s['stretching'] , many = True)
		return {
			"stretching" : sw.data
		}

	def get_object(self):
		gen = Generator(self.request.user)
		gen.generate()
		return {
			**self.get_warmup(gen),
			**self.get_main(gen),
			**self.get_stretching(gen)

		}
	def get(self , request , *args , **kwargs):
		logger = logging.getLogger(__name__)
		logger.info("Workout GET")
		gen = Generator(request.user)
		with open("workout/data.json") as f:
			a = json.load(f)
		return Response(a)
