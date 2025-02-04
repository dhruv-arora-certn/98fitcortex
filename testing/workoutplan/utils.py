from workoutplan import levels
from workoutplan.goals import Goals
from workoutplan import resistance_data
from workoutplan import shared_globals

from django.db.models import Q

import random
import copy
import collections
import enum
import functools
import logging

type_list = ["WeightLoss" , "WeightGain" , "MuscleGain" , "MaintainWeight"]

days = collections.namedtuple("Days" , ["cardio","rt","cs" , "total"])

Novice = collections.namedtuple("Novice" , type_list)
Beginner = collections.namedtuple("Beginner" , type_list)
Intermediate = collections.namedtuple("Intermediate" , type_list)

WeightGain = collections.namedtuple("WeightGain" , ["days"])
WeightLoss = collections.namedtuple("WeightLoss" , ["days"])
MuscleGain = collections.namedtuple("MuscleGain" , ["days"])
MaintainWeight = collections.namedtuple("MaintainWeight" , ["days"])

NoviceDays = Novice(
    WeightLoss(
        days(5,0,5,5)
    ),
    WeightGain(
        days(3,0,3,3)
    ),
    MuscleGain(
        days(4,0,4,4)
    ),
    MaintainWeight(
        days(4,0,4,4)
    )
)

BeginnerDays = Beginner(
    WeightLoss(
        days(5,2,2,5)
    ),
    WeightGain(
        days(2,3,2,5)
    ),
    MuscleGain(
        days(2,3,2,5)
    ),
    MaintainWeight(
        days(3,2,2,5)
    )
)

IntermediateDays = Intermediate(
    WeightLoss(
        days(5,2,2,5)
    ),
    WeightGain(
        days(2,6,2,6)
    ),
    MuscleGain(
        days(2,6,2,6)
    ),
    MaintainWeight(
        days(3,2,2,5)
    )
)

ct = collections.namedtuple(
    "ConditionalTraining" , ["novice" , "beginner" , "intermediate"]
)

ConditionalTrainingDays = ct(
    NoviceDays , BeginnerDays , IntermediateDays
)


class Luggage:
    '''
    Randomly select objects from `items` so that they have a maximum cumulative weight of `weight`

    Parameters
    ----------
    `weight` : `int` 
            The maximum cumulative property that all the items should have
    `items` : list
            List of items from which the selections have to be made
    `key` :  str
            The `attribute` on the objects in list which will be used to determine the weight
    `multiplier` : int
            The multiplier for the weight of each item
    `batchSize` : int
            The minimum amount of items to be selected from each selection
    '''

    def __init__(self , weight , items , key , multiplier = 1 ,randomize = True , batchSize = 5):
        self.weight = weight
        self.items = set(items)
        self.key = key
        self.multiplier = multiplier
        self.randomize = randomize
        self.packed = set()
        self.batchSize = batchSize
        self.max_iterations = 60
        self.logger = logging.getLogger(__name__)
        self.logger.debug("State of Luggage %s"%self.__dict__)


    def pickAndPack(self):
        selectedWeight = sum(getattr(e , self.key)*self.multiplier for e in self.packed)
        counter = 0
        while selectedWeight < self.weight and counter < self.max_iterations:
            batch = random.sample(
                self.items.difference(self.packed) ,
                min(self.batchSize , len(self.items.difference(self.packed)))
            )
            self.logger.debug("Selected Weight :%s"%selectedWeight)
            for e in batch:
                assert isinstance(getattr(e,self.key) , int) , "Not an integer %s - %s"%(getattr(e , self.key) , type(getattr(e , self.key)))
                if selectedWeight + getattr(e , self.key)*self.multiplier <= self.weight :
                    selectedWeight += getattr(e , self.key)*self.multiplier
                    self.packed.add(e)
            counter += 1
        return self


def get_resistance_filter( user , day_number):
    assert user.level_obj is not levels.Novice

    r =  getattr(user.level_obj.Resistance , user.goal.__name__)
    return getattr(r , "D%s"%(day_number))

def get_days(cls_obj , category):
        goal = cls_obj.user.goal
        if goal == Goals.WeightLoss:
            return getattr(category,"WeightLoss").days

        elif goal == Goals.WeightGain:
            return getattr(category,"WeightGain").days

        elif goal == Goals.MuscleGain:
            return getattr(category,"MuscleGain").days

        elif goal == Goals.MaintainWeight:
            return getattr(category,"MaintainWeight").days


def get_category_decorator(category):
    def decorator(fn):
        def applyCat(cls_obj):
            return get_days(cls_obj , category)
        return applyCat
    return decorator

filter_tuple = collections.namedtuple("filter_" , ["filter" , "count"])

class CardioStretchingFilter(enum.Enum):
    '''
    A Container for holding filters for cardio stretching 
    '''
    QUADS = filter_tuple(
        filter = Q(muscle_group_name = "Quadriceps"),
        count = 1
    )
    CHEST = filter_tuple(
        filter = Q(muscle_group_name  = "Chest"),
        count = 1
    )
    GLUTES = filter_tuple(
        filter = Q(muscle_group_name = "Glutes"),
        count = 1
    )
    BACK = filter_tuple(
        filter = Q(muscle_group_name = "Back"),
        count = 1
    )

def get_novice_cardio_sets_reps_duration(level , goal , user_workout_week, cardio = True , rt = False):
    '''
    Return the sets and reps for cardio exercises of a cardio novice user
    '''
    assert level == levels.Novice , "User should be novice"
    sets = 2
    week = user_workout_week
    if 1 <= week <= 2:
        reps = 8
    elif 3 <= week <= 5:
        reps = 10
    elif week >= 6:
        reps = 12
    duration = 900
    return sets , reps , duration

def get_beginner_cardio_sets_reps_duration(level , goal , user_workout_week, cardio = True , rt = False):
    '''
    Get `sets`,`reps`, and `duration` for cardio for a user whose fitness level is beginner
    '''

    assert level == levels.Beginner , "User should be beginner"

    if goal == Goals.WeightLoss:
        if cardio and rt:
            sets = 2
            duration = 900
        else:
            sets = 4
            duration = 1500

    if goal == Goals.WeightGain or goal == Goals.MuscleGain:
        sets = 3
        duration = 900

    if goal == Goals.MaintainWeight:
        sets = 3
        duration = 1200

    reps = None
    return sets , reps  ,duration

def get_intermediate_cardio_sets_reps_duration(level , goal , user_workout_week, cardio = True , rt = False):
    '''
    Get `sets`,`reps` and `duration` for cardio for a user whose fitness level is intermediate
    '''

    assert level == levels.Intermediate , "User should be of intermediate level"

    if goal == Goals.WeightLoss:
        if cardio and rt:
            sets = 2
            duration = 300
        else:
            sets = 4
            duration = 1800

    elif goal == Goals.WeightGain or Goals.MuscleGain:
        sets = 2
        duration = 1200

    elif goal == Goals.MaintainWeight:
        sets = 3
        duration = 1500

    return sets , None ,duration

def get_cardio_sets_reps_duration( level , goal , user_workout_week, cardio = True , rt = False):
    '''
    Get sets, reps and duration for which a cardio workout has to be performed

    Parameters
    ----------
    `level` : `workout.levels`
    `goal`: `epilogue.goals`
    `user_workout_week` : int
                Week for which the workout has to be generated
    `cardio` : bool
            Indicator whether cardio is being suggested on that day
    `rt` : bool
            Indicator whether  resistance training is being suggested on that day

    Returns
    -------
    container : `collections.namedtuple`
        A namedtuple consisting of the sets, reps and duration
    '''
    if level == levels.Novice:
        val =  get_novice_cardio_sets_reps_duration(level,goal , user_workout_week, cardio , rt)
    elif level == levels.Beginner:
        val =  get_beginner_cardio_sets_reps_duration(level,goal , user_workout_week, cardio ,rt)
    elif level == levels.Intermediate:
        val = get_intermediate_cardio_sets_reps_duration(level,goal , user_workout_week, cardio , rt)
    container = collections.namedtuple("container" , ["sets" , "reps" , "duration"])
    return container(*val)

def get_cardio_intensity_filter_for_warmup(user):
    '''
    Get the intensity and duration for warmup

    Returns
    -------

    A list of dictionaries containing the `filter` and `duration` to get the cardio exercises
    '''
    if user.is_novice():
        return [{
            "filter" : Q(exercise_level = "Low"),
            "duration" : 300
        }]

    elif user.is_beginner():
        return [
            {
                "filter" : Q(exercise_level = "Low"),
                "duration" : 150
            },
            {
                "filter" : Q(exercise_level = "Moderate"),
                "duration" : 150
            }
        ]

    elif user.is_intermediate():
        return [
            {
                "filter" : Q(exercise_level = "Low"),
                "duration" : 60
            },
            {
                "filter" : Q(exercise_level = "Moderate"),
                "duration" : 60
            },
            {
                "filter" : Q(exercise_level = "High"),
                "duration" : 180
            }
            ]


class DummyWarmup:
    '''
    Container for holding Dummy warmup exercises
    '''
    duration = 300
    module_name = "WarmupCoolDownMobilityDrillExercise".lower()
    id = 0

    def __str__(self):
        return self.workout_name
    def __repr__(self):
        return self.workout_name
    def __init__(self,cardio):
        self.workout_name = cardio.workout_name
        self.machine_name = cardio.machine_name

class DummyCoolDown:
    '''
    Container for holding Dummy cooldown exercises
    '''
    module_name = "WarmupCoolDownMobilityDrillExercise".lower()
    id = 0

    def __init__(self , duration, workout_name):
        self.duration = duration
        self.workout_name = workout_name


def filter_key_from_q(q_obj , key_to_escape):
    '''
    Remove a key from django Q object
    '''
    new_children = []
    q_obj = copy.copy(q_obj)
    for e in q_obj.children:
        #e is a tuple
        if isinstance(e , Q):
            e = filter_key_from_q(e , key_to_escape)
            new_children.append(e)
        elif e[0] != key_to_escape:
            new_children.append(e)

    q_obj.children = new_children
    return q_obj
