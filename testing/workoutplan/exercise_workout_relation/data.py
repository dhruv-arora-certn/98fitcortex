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


def check_activity_fitness_compat(activity , fitness):
    act , periodize = activity_level_map[1][0]
    changed = False
    if not act == activity:
        changed = True
    return act,periodize,changed
