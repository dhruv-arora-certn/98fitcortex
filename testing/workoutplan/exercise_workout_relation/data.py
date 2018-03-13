from workoutplan import levels
from dietplan.activity import ActivityLevel
from collections import namedtuple


activity_tuple = namedtuple("Activity", ["name" , "value"])



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

periodization_map = [
    ( ActivityLevel.lightly_active, levels.Beginner),
    ( ActivityLevel.moderately_active , levels.Beginner) ,
    ( ActivityLevel.moderately_active , levels.Intermediate),
]


def is_periodized(fitness, activity):
    '''
    Given a pair of (fitness,activity) return if it is periodized.
    Checks against the (fitness,activity) values in periodization_map
    '''
    try:
        index = periodization_map.index((activity,fitness))
    except ValueError as e:
        return False
    else:
        return True

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
    Return the new activity level of the user.
    '''
    to_periodize = is_periodized(fitness, activity)
    new_activity = get_new_activity(fitness,activity)
    print("To periodize ", to_periodize)
    print("New Activity ",new_activity )
    if not to_periodize:
        if new_activity != activity:
            return new_activity
        return activity
    else:
        if periodization_weeks < 12:
            return activity
        return new_activity


def check_activity_fitness_compat(activity , fitness):
    act_index = [
        ActivityLevel.sedentary , ActivityLevel.lightly_active, ActivityLevel.moderately_active, ActivityLevel.very_active
    ].index(activity)

    fit_index = [
        levels.Novice ,levels.Beginner, levels.Intermediate        
    ].index(fitness)

    act , periodize = activity_level_map[act_index][fit_index]
    return act, periodize
