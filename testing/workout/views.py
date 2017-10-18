from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework import permissions
from epilogue.authentication import CustomerAuthentication
from workout.models import *
from workout.serializers import *
from epilogue.utils import get_week , get_day
import random

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
