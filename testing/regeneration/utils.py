from . import constants
from . import models

from epilogue.models import GeneratedDietPlan
from epilogue.utils import get_week , get_year

from workout.models import GeneratedExercisePlan

import itertools
import logging


def get_logger():
    return logging.getLogger(__name__)

def get_window_tuples(week = get_week() , year = get_year()):
    '''
    Get the tuples of (year,week) for which plans can be regenerated
    '''
    return [
        (y , w) for w,y in zip(
            [
                week + i for i in range(0, 1 + constants.REGENERATION_WINDOW)
            ],
            itertools.repeat(year , constants.REGENERATION_WINDOW + 1)
        )
    ]


def create_regeneration_node(_type, user, year , week):
    '''
    Create a database record for regeneration 

    Parameters
    ----------
    `_type` : {'diet','workout'}
            Indicate the type of plan that has to be regeneratedof  
    `year` : int
            The year for which the plan has to be regenerated
    `week` : int
            Week of the year for which the plan has to be regenerated

    Returns
    ------
    obj : instance of `regeneration.models.RegenerationLog`
    '''
    logger = get_logger()
    logger.debug("++++++++++++++++ Creating Object")
    obj,created = models.RegenerationLog.objects.get_or_create(
        type = _type,
        year = year,
        week = week,
        customer = user
    )
    if not created and obj.regenerated:
        obj.toggleStatus()

    return obj

def create_diet_regeneration_node(user,year,week):
    '''
    Create a database record for diet regeneration
    '''
    logger = get_logger()
    dietplan = GeneratedDietPlan.objects.filter(
        year = year,
        week_id = week,
        customer = user
    )
    count = dietplan.count()
    logger.debug("Reaching Diet Regeneration Stage count:%d , week:%d , year:%d"%(count,week,year))
    logger.debug(str(dietplan.query))
    if count:
        return create_regeneration_node(
            "diet" ,user ,year , week
        )
    return None

def create_workout_regeneration_node(user,year,week):
    '''
    Create a database record for workout regeneration
    '''
    logger = get_logger()
    logger.debug("Reaching Workout Regeneration Stage")

    workoutplan = GeneratedExercisePlan.objects.filter(
        year = year,
        week_id  = week,
        customer = user
    )
    if workoutplan.count():
        return create_regeneration_node(
            "workout" , user ,year , week
        )
    return None
