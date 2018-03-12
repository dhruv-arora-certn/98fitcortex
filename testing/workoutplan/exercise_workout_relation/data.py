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
        (ActivityLevel.moderately_active, 0) , (ActivityLevel.moderately_active, 0) , (ActivityLevel.moderately_active, 1)
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
def check_activity_fitness_compat(activity , fitness):
    act_index = [
        ActivityLevel.sedentary , ActivityLevel.lightly_active, ActivityLevel.moderately_active, ActivityLevel.very_active
    ].index(activity)

    fit_index = [
        levels.Novice ,levels.Beginner, levels.Intermediate        
    ].index(fitness)

    act , periodize = activity_level_map[act_index][fit_index]
    return act, periodize


def upgrade_activity(activity , fitness , weeks_in_fitness):
    new_activity , periodize= check_activity_fitness_compat(activity , fitness)
    if not periodize:
        print("Not periodize")
        return new_activity
    else:
        if weeks_in_fitness < duration:
            print("Weeks less")
            return activity
        else:
            print("Last")
            return new_activity

