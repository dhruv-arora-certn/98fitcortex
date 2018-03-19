from django.shortcuts import render
from django.core.cache import cache

# Create your views here.
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions

from rest_framework_bulk import ListBulkCreateAPIView

from epilogue.authentication import CustomerAuthentication
from epilogue.utils import get_week , get_day , BulkDifferential , is_valid_week
from epilogue.permissions import WeekWindowAccessPermission

from workout.models import *
from workout.serializers import *
from workout.utils import get_day_from_generator , workout_regenerator
from workout.persister import WorkoutWeekPersister
from workout import renderers

from workoutplan.generator import Generator
from workoutplan.utils import get_cardio_sets_reps_duration

import regeneration.views as regeneration_views

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

        if kwargs['day'] in ('6' , '7'):
            return Response([])

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

class DashboardWorkoutTextView(generics.GenericAPIView):
    authentication_classes = [CustomerAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self , *args , **kwargs):
        user = self.request.user
        string = "5 Minutes Warmup, %d Minutes Cardio"

        cardio_duration = get_cardio_sets_reps_duration(user.level_obj , user.goal , user.user_relative_workout_week)

        string = string%(cardio_duration.duration/60)

        return Response({
            "workout" : string
        })


class CustomerInjuryView(ListBulkCreateAPIView , BulkDifferential):
    authentication_classes = [CustomerAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomerInjurySerializer
    mapper = {
        1 : "lower_back",
        2 : "back",
        3 : "knee",
        4 : "ankle",
        5 : "elbow",
        6 : "wrist",
        7 : "shoulder"
    }

    class BulkMeta:
        attr_name = "injury_name"
    
    def get_queryset(self):
        return self.request.user.injuries.all()

    def getPartition(self , request):
        old = list(request.user.injuries.all())
        new = [CustomerInjury(customer = request.user , injury_name = e.get('injury_name')) for e in request.data ]
        return self.getToDelete( old , new) , self.getToAdd( old , new )

    def post(self , request , *args , **kwargs):
        bulk = isinstance(request.data , list)
        if bulk:
            toDelete , toAdd = self.getPartition(request)

            for e in toDelete:
                e.delete()
            for e in toAdd:
                e.save()
        objs = request.user.injuries.all()
        data = self.serializer_class(objs , many = True)
        return Response(
            data.data ,
            status = status.HTTP_201_CREATED
        )


class GenerateWorkoutView(generics.GenericAPIView):
    authentication_classes = [CustomerAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = GeneratedExercisePlan
    logger = logging.getLogger(__name__)

    def generate_workout(self):
        g = Generator(
            self.request.user
        )
        g.generate()

        self.new_workout = WorkoutWeekPersister(
            g,
            self.kwargs.get('week_id')
        )
        self.new_workout.persist()
        return self.new_workout.model_obj


    def get_object_hook(self):
        workout_week = GeneratedExercisePlan.objects.filter(
            customer = self.request.user,
            week_id = int(self.kwargs.get('week_id')),
            year = int(self.kwargs.get('year'))
        ).last()

        if workout_week:
            return workout_week

        return self.generate_workout()

    def filtered_queryset(self , qs):
        return qs.exercises.filter(
            day = int(self.kwargs.get('day'))
        )

    def categorise_data(self,data):
        keys = set([e.get('mod_name') for e in data])
        new_data = {}

        for e in keys:
            new_data.update({e:[]})

        def assign(a):
            new_data[a.get('mod_name')].append(a)

        [assign(e) for e in data]

        return new_data

    def get(self , request , *args , **kwargs):
        year = int(self.kwargs.get('year'))
        week = int(self.kwargs.get('week_id'))
        if not is_valid_week(year , week):
            raise exceptions.PermissionDenied({
                "message" : "You cannot access this week's workout plan"
            })

        obj = self.get_object()
        obj = self.filtered_queryset(obj)
        data = GeneratedExercisePlanDetailsSerializer(obj , many = True)

        return Response(self.categorise_data(data.data))


class RegenerableWorkoutView( GenerateWorkoutView , regeneration_views.RegenerableView):

    def check_and_update_fitness(self,request):
        '''
        Check if the fitness needs to be updated for the workout week requested
        '''
        pass

    def check_and_update_activity_level(self,request):
        '''
        Check if the activity level needs to be updated for the workout week requested
        '''
        pass

    def before_request_hook(self,request, *args, **kwargs):
        '''
        Add calls to functions that must be run before the request is responded to
        '''
        self.check_and_update_fitness(request, *args, **kwargs)
        return
    
    def get_regenerate_log_filter(self):
        return {
            'customer' : self.request.user,
            'year' : self.kwargs.get('year'),
            'week' : self.kwargs.get("week_id"),
            'regenerated' : False,
            'type' : 'workout'
        }

    def regeneration_hook(self , obj):
        logger = logging.getLogger("regeneration") 
        logger.debug("Calling Regeneration Hook")
        workout , status =  workout_regenerator(obj)
        
        if status:
            self.regen_obj.toggleStatus()
        return workout
    
    def get(self , request , *args, **kwargs):
        self.before_request_hook(request , *args, **kwargs)
        year = int(self.kwargs.get('year'))
        week = int(self.kwargs.get('week_id'))

        if not is_valid_week(year,week):
            raise exceptions.PermissionDenied({
                "message" : "You cannot access this week's plan"
            })
        obj = self.get_object()
        objs = self.filtered_queryset(obj)

        data = GeneratedExercisePlanDetailsSerializer(objs , many = True)
        return Response(self.categorise_data(data.data))
