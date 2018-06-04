from django.dispatch import receiver

from . import signals
from .utils import get_window_tuples , create_diet_regeneration_node , create_workout_regeneration_node

import epilogue.constants

from epilogue import cache_utils

import logging

@receiver(signals.diet_regeneration)
def diet_regenerator(sender , *args , **kwargs):
    user = kwargs.pop('user')
    logger = logging.getLogger(__name__)
    logger.debug("Received Diet Regeneration")

    #Invalidate Cache
    cache_utils.invalidate_cache(user, cache_utils.modules.DIET_DASHBOARD_STRING)
    eligible_window = get_window_tuples()
    return [
        create_diet_regeneration_node(user,*t) for t in eligible_window
    ]

@receiver(signals.specific_diet_regeneration)
def specific_diet_regeneration(sender, *args, **kwargs):
    user = kwargs.pop("user")
    week = kwargs.pop("week")
    year = kwargs.pop("year")

    cache_utils.invalidate_cache(user, cache_utils.module.DIET_DASHBOARD_STRING)
    eligible_window = get_window_tuples(week = week , year = year)
    
    return [
        create_diet_regeneration_node(user, *t) for t in eligible_window
    ]


@receiver(signals.workout_regeneration)
def workout_regenerator(sender , *args, **kwargs):
    user = kwargs.pop('user')
    eligible_window = get_window_tuples()

    logger = logging.getLogger(__name__)
    logger.debug("Received Workout Regeneration")

    return [
        create_workout_regeneration_node(user,*t) for t in eligible_window
    ]
