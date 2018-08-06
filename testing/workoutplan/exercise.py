import random
import logging

from django.core.cache import cache
from django.db.models import Q
from django.conf import settings

from workout import models
from workoutplan.utils import Luggage , get_cardio_sets_reps_duration  , filter_key_from_q
from workoutplan import shared_globals
from workoutplan import periodization

random.seed()

class ExerciseBase:
    '''
    Base class for building exercises.

    Notes
    -----
    It selects items using `Luggage` for selecting exercises  
    '''

    def __init__(self , user , duration):
        self.logger = logging.getLogger(__name__)
        self.user = user
        self.duration = duration
        self.cache_key = self.__class__.__name__
        self.selected = []
        self.multiplier = 1

    def build(self):
        self.logger.info("State of %s : %s"%(self.__class__.__name__ , self.__dict__))
        items = self.get_items()
        self.logger.debug("Items Length  in %s %d"%(self.__class__.__name__ ,  len(items)))
        l = Luggage(
            self.duration,
            items,
            "duration",
            self.multiplier
        ).pickAndPack()
        self.selected.extend(l.packed)
        return self

    def get_location_filter(self):
        if hasattr(shared_globals , "location_pref"):
            return getattr(shared_globals.location_pref , "filter" , Q())
        return Q()

    def get_items(self):
        model_list = self.model.objects.filter(self.get_location_filter())
        if settings.CACHE_WORKOUT:
            logging.info("Using Cache")
            return list(cache.get_or_set(self.cache_key , model_list))
        return list(model_list)

class FloorBasedCardio(ExerciseBase):

    def __init__(self , user , duration , sets=0 , reps=0):
        super().__init__(user , duration)
        self.model = models.CardioFloorExercise
        self.sets = sets
        self.reps = reps

    def build(self):
        self.multiplier = self.sets

        #get the filter for selecting exercises
        self.periodised_filters = periodization.get_cardio_periodized(self.user.level_obj , self.user.user_relative_workout_week)
        self.selected = []

        for e in self.periodised_filters:
            items = self.model.objects.filter(e.get("filter"))
            duration = self.duration * e.get("ratio")
            print("Luggage Duration %d"%duration )
            l = Luggage(
                duration,
                items,
                "duration",
                self.multiplier,
                batchSize = 1
            ).pickAndPack()
            self.selected.extend(l.packed)

        def add_sets_reps(x):
            setattr(x , "sets" , self.sets)
            setattr(x , "reps" , self.reps)
            return x

        self.selected = list(map(
            add_sets_reps , self.selected
        ))
        return self

class TimeBasedCardio(ExerciseBase):

    def __init__(self , user , duration , sets , reps):
        super().__init__( user , duration )
        self.model = models.CardioTimeBasedExercise

    def build(self):
        self.srd_container = get_cardio_sets_reps_duration(self.user.level_obj, 
                self.user.goal, 
                self.user.user_relative_workout_week,
                )
        self.selected.append(random.choice(self.get_items()))

        def add_sets_reps(x):
            setattr(x , "sets" , 1)
            setattr(x , "reps" , 1)
            setattr(x , "duration" , self.srd_container.duration)
            return x

        self.selected = list(
            map(
                add_sets_reps , self.selected
            )
        )
        return self

class ResistanceTraining(ExerciseBase):

    def __init__( self , user , count , filters):
        self.filter = filters
        self.model = models.ResistanceTrainingExercise
        self.count = count
        self.selected = []

    def get_items(self):
        return list(self.model.objects.filter(self.filter))

    def build(self):
        items = self.get_items()
        selected_items = random.sample(items , self.count)
        self.selected.extend(selected_items)
        return self


class CoreStrengthening(ExerciseBase):

    def __init__(self , user , duration = 0, **kwargs):
        super().__init__(user , duration)
        self.model = models.NoviceCoreStrengthiningExercise
        self.multiplier = 2

class Warmup(ExerciseBase):

    def __init__(self , user , duration = 300 , modelToUse = None , filterToUse = Q() ,**kwargs):
        assert modelToUse , "Model Should be defined"
        super().__init__(user , duration)
        self.model = modelToUse
        self.filter = filterToUse
        #self.cache_key = "%s_%s"%(self.model.__name__ , "_".join("%s_%s"%(i,e) for i,e in filterToUse.children))

    def get_items(self):
        model_list = list(self.model.objects.filter(self.filter))
        if settings.CACHE_WORKOUT:
            return  cache.get_or_set(self.cache_key ,model_list )
        return model_list


class Stretching(ExerciseBase):

    def __init__(self , user , filterToUse = Q() , count = 1):
        self.user = user
        self.filterToUse = filter_key_from_q(filterToUse , "exercise_type")
        self.model = models.StretchingExercise
        #self.cache_key = "%s_%s"%(self.model.__name__ , "_".join("%s_%s"%(i,e) for i,e in filterToUse.children))
        self.selected = []
        self.multiplier = 2
        self.count = count

    def get_items(self):
        model_list =  list(self.model.objects.filter(self.filterToUse))
        if settings.CACHE_WORKOUT:
            return cache.get_or_set(self.cache_key , model_list) 
        return model_list 

    def build(self):
        items = self.get_items()
        if self.count == 1:
            choice = random.choice(items)
            self.selected.append(choice)
        elif self.count > 1:
            choice = random.sample(items , self.count)
            self.selected.extend(choice)
        [setattr(e,"duration" ,15 * self.multiplier) for e in self.selected]
        return self
