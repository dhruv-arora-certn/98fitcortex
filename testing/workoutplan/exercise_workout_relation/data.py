from workoutplan import levels

from dietplan.activity import ActivityLevel

from regeneration.signals import diet_regeneration, specific_diet_regeneration

from collections import namedtuple

from django import apps

import logging
import collections


activity_tuple = namedtuple("Activity", ["name" , "value"])

logger = logging.getLogger("activity_upgrade")   

##### Activity-Level Validation Map
# 4x3 matrix
# Rows(Lifestyle/ActivityLevel) : Sedentary, LightlyActive, ModeratelyActive, VeryActive
# Columns(Fitness Level) : Novice , Beginner, Intermediate
# activity_level_map[1,1] is retrieval of Compatibility of LightlyActive and Beginner
#

activity_level_map = [
    [
        (ActivityLevel.lightly_active, 0) , (ActivityLevel.lightly_active, 1) , ()
    ],
    [
        (ActivityLevel.lightly_active, 0) , (ActivityLevel.moderately_active, 0) , (ActivityLevel.moderately_active, 1)
    ],
    [
        (ActivityLevel.moderately_active, 0) , (ActivityLevel.moderately_active, 0) , (ActivityLevel.very_active, 1)
    ],
    [
        (ActivityLevel.very_active, 0) , (ActivityLevel.very_active, 0) , (ActivityLevel.very_active, 0)
    ]
]

periodization_map = {
    ( ActivityLevel.lightly_active, levels.Beginner) : range(1,10),
    ( ActivityLevel.moderately_active , levels.Beginner) :  range(1,10),
    ( ActivityLevel.moderately_active , levels.Intermediate) : range(1,9) ,
}

def is_periodized(fitness, activity):
    '''
    Given a pair of (fitness,activity) return if it is periodized.
    Checks against the (fitness,activity) values in periodization_map
    '''
    if (activity,fitness) in periodization_map:
        return True
    return False

def get_new_activity(fitness, activity):
    '''
    Given a pair of (fitness,activity) return the new activity level
    Maps the (fitness,activity) pair against the activity_level_map
    '''
    act_index = [
        ActivityLevel.sedentary , ActivityLevel.lightly_active, ActivityLevel.moderately_active, ActivityLevel.very_active
    ].index(activity)

    fit_index = [
        levels.Novice ,levels.Beginner, levels.Intermediate        
    ].index(fitness)
    return activity_level_map[act_index][fit_index]

def upgrade_activity(fitness, activity, periodization_weeks):
    '''
    Given a pair of (fitness,activity) determine if the activity is to be
    upgraded or not.

    Parameters
    ----------
    periodization_weeks : weeks into that particular fitness level. If 
    an offset has been provided, it needs to be removed

    Return the new activity level of the user.
    '''
    fit_act = (fitness,activity)
    to_periodize = is_periodized(*fit_act)
    new_activity = get_new_activity(*fit_act)[0]
    logger.debug("To periodize %s"%str(to_periodize))
    logger.debug("New Activity %s"%str(new_activity ))
    if to_periodize:
        if periodization_weeks in periodization_map[(activity,fitness)]:
            return activity
        return new_activity
    else:
        if new_activity != activity:
            return new_activity
        return activity

def _upgrade_user_activity(user, new_activity, context):
    '''
    Add new activity level record for the user.
    Send a signal for diet regeneration.
    '''
    logger.debug("Upgrading User from %0.2f to %0.2f"%(user.new_latest_activity , new_activity))
    try:
        record = user.activitylevel_logs.create(
            lifestyle = str(new_activity),
            week = context.get("week"),
            year = context.get("year")
        )
    except Exception as e:
        raise
        return user
    else:
        specific_diet_regeneration.send(
            sender = apps.apps.get_model("epilogue","Customer"),
            user = user,
            **context
        )
    return user

def upgrade_user(user , week = None, context = collections.defaultdict(int)):
    '''
    Function to Upgrade User's activity level based on his workout week
    Return the upgraded user
    '''
    if not week:
        week = user.user_relative_workout_week
    activity_level = float(user.activity_level_to_use(
        **context
    ))
    fitness_level = user.fitness_level_to_use_obj(
        **context
    )
    activity = upgrade_activity( fitness_level, activity_level, week ) 
    logger.debug("User Week %d"%week)
    if activity != user.new_latest_activity:
        return _upgrade_user_activity(user,activity,context)
    return user
