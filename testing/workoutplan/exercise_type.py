import random
import operator
import itertools
import enum
import collections
import logging

from workout import models
from workoutplan import exercise
from workoutplan import shared_globals
from .utils import Luggage , CardioStretchingFilter , get_cardio_sets_reps_duration , get_cardio_intensity_filter_for_warmup , DummyWarmup , filter_key_from_q
from .alternator import alternate_gen


from django.core.cache import cache
from django.db.models import Q

class Base():

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        pass

class Warmup(Base):
    _type = "warmup"
    duration = 300

    def __init__(self , user , mainCardio = None , bodyPartInFocus = Q() , make_cardio = False):
        super().__init__()
        self.user = user
        self.mainCardio = mainCardio
        if hasattr(mainCardio.resistance_filter , "bodyPartInFocus"):
            self.bodyPartInFocus = mainCardio.resistance_filter.bodyPartInFocus.filter
        else:
            self.bodyPartInFocus = Q()
        self.selected = []

    def decideWarmup(self):
        '''
        Decide Which Function is to be called For generating the Warmup
        The function is assigned to the object rather than returned,
        Self is returned instead
        This will enable me to perform chaining and allow subsequent functions to use the attribute
        '''
        if self.mainCardio.cardioType== exercise.FloorBasedCardio:
            self.logger.info("Decided Warmup Floor Based")
            return self.floor_based_cardio()
        elif self.mainCardio.cardioType == exercise.TimeBasedCardio:
            self.logger.info("Decided Warmup Time Based")
            return self.time_based_cardio()
        else:
            return self.normal_warmup_cooldown()

    def floor_based_cardio(self):
        '''
        To be used in the case where main exercise is Floor Based Cardio
        '''
        return self.normal_warmup_cooldown()

    def normal_warmup_cooldown(self):
        '''
        To be used in the case where a normal Warm Up and Cool Down is to be generated
        '''
        filters = get_cardio_intensity_filter_for_warmup(self.user)
        modelToUse = models.WarmupCoolDownMobilityDrillExercise
        l = []

        for e in get_cardio_intensity_filter_for_warmup(self.user):
            self.logger.debug(e.get('filter') & self.bodyPartInFocus)
            warmup = exercise.Warmup(
                self.user,
                duration = e.get('duration'),
                modelToUse = modelToUse,
                filterToUse = e.get('filter') & self.bodyPartInFocus
            ).build()
            l.extend(warmup.selected)
        return  l

    def rt_warmup(self):
        pass

    def time_based_cardio(self):
        class Warmup:
            duration = 300
            def __str__(self):
                return self.workout_name
            def __repr__(self):
                return self.workout_name
            def __init__(self,name):
                self.workout_name = name

        return list(map(lambda x : DummyWarmup(x) , [
            e for e in self.mainCardio.cardio
        ]))

    def build(self):
        self.selected = {
            "warmup" : self.decideWarmup()
        }
        return self

    def as_dict(self):
        return {
            "warmup" : self.selected
        }


class Main(Base):
    _type = "main"
    cardioTypeGen = alternate_gen([exercise.FloorBasedCardio , exercise.TimeBasedCardio])

    def __init__(self , user , resistance_filter = None , make_cardio = False , make_cs = False):
        super().__init__()
        self.user = user
        self.make_cardio = make_cardio

        if self.make_cardio:
            self.cardioType = next(Main.cardioTypeGen)
        else:
            self.cardioType = None
        self.resistance_filter = resistance_filter
        self.make_cs = make_cs
        self.conditionalType = None

        if resistance_filter:
            self.conditionalType = exercise.ResistanceTraining
        elif self.make_cs:
            self.conditionalType = exercise.CoreStrengthening

        if self.cardioType == exercise.FloorBasedCardio and not self.user.is_novice():
            self.srd_container = get_cardio_sets_reps_duration(user.level_obj , user.goal , user.user_relative_workout_week , make_cardio , bool(resistance_filter))
            self.duration = self.srd_container.duration
            self.sets = self.srd_container.sets
            self.reps = self.srd_container.reps
        else:
            self.duration = 900
            self.sets = 0
            self.reps = 0
        self.logger.debug("Cardio Type %s"%(self.cardioType))

    def buildCardio(self):
        self.logger.debug("Duration is %s"%self.duration)
        self.logger.debug("CardioType is %s"%self.cardioType)
        self._cardio = self.cardioType(
            self.user,
            self.duration,
            self.sets,
            self.reps
        )
        self._cardio.build()
        return self._cardio.selected

    def buildResistanceTraining(self):
        self.conditionalType = exercise.ResistanceTraining
        l = []
        for e in self.resistance_filter.filters:
            rt = exercise.ResistanceTraining(
                user = self.user,
                count = e.get('count' , 1),
                filters = e.get('filter')
            )
            rt.build()
            for obj in rt.selected:
                setattr(obj, "reps" , self.resistance_filter.reps)
                setattr(obj , "sets" , self.resistance_filter.sets)
            l.extend(rt.selected)
        return l

    def buildCoreStrengthening(self):
        self.duration = 300
        self.conditionalType = exercise.CoreStrengthening
        core = exercise.CoreStrengthening(
            user = self.user,
            duration = self.duration,
        )
        core.build()
        return core.selected

    def buildRT(self):
        if self.resistance_filter :
            self.rt = self.buildResistanceTraining()
        if self.make_cs:
            self.cs =  self.buildCoreStrengthening()
        return

    def build(self):
        '''
        Build exercises after assembly
        '''
        self.selected = {}
        if self.make_cardio:
            self.cardio = self.buildCardio()
            self.selected = {
                "cardio" : self.cardio ,
            }

        self.buildRT()
        if self.resistance_filter:
            self.selected.update({
                "resistance_training" : self.rt
            })
        if self.make_cs:
            self.selected.update({
                "core_strengthening" : self.cs
            })
        return self.selected

    def as_dict(self):
        return {
            "cardio" : self.cardio,
            "resistance_training" : self.rt
        }


class CoolDown(Base):
    _type = "cooldown"
    def __init__(self):
        super().__init__()
        pass

class Stretching(Base):
    _type = "stretching"
    def __init__(self , user , resistance_filter = None , cardio = False):
        super().__init__()
        self.user = user
        self.resistance_filter = resistance_filter
        self.cardio = cardio

    def build_rt(self):
        l = []
        for e in self.resistance_filter.filters:
            stretching = exercise.Stretching(
                user = self.user,
                filterToUse = e.get('filter'),
                count = e.get('stretching_count',1)
            )
            stretching.build()
            l.extend(stretching.selected)
        return l

    def build_cardio(self):
        #return CardioStretchingFilter
        l = []
        for e in CardioStretchingFilter:
            stretching = exercise.Stretching(
                user = self.user,
                filterToUse = e.value.filter
            )
            stretching.build()
            l.extend(stretching.selected)
        return l


    def build(self):
        l = {"stretching" : set()}
        if self.resistance_filter:
            self.rt_stretching = self.build_rt()
            l['stretching'].update(self.rt_stretching)

        if self.cardio:
            self.cardio_stretching = self.build_cardio()
            l['stretching'].update(self.cardio_stretching)
        l['stretching'] = list(l['stretching'])
        self.selected = l
        return self

class CoolDown(Base):
    pass
