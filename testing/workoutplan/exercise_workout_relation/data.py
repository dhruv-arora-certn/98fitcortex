from workoutplan import levels
from dietplan import activity
from collections import namedtuple


activtiy_tuple = namedtuple("name" , "value")

Sedentary = activity_tuple(
    "Sedentary" , 
    activity.ActivityLevel.sedentary
)

LightlyActive = activity_tuple(
    "LightlyActive",
    activity.ActivityLevel.lightly_active
)

ModeratelyActive = activity_tuple(
    "Moderately Active",
    activity.ActivityLevel.moderately_active
)

activity_level_map = {
    levels.Novice : [
        (
            Sedentary , 0
        ),
        (
            LightlyActive , 1
        )
    ]
}
