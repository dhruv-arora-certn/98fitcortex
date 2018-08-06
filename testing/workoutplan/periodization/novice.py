import functools

from django.db.models import Q

@functools.lru_cache()
def get_novice_cardio_periodized(user_week_no):

    #assert 1 <= user_week_no <= 6 , "Novie Week no is between 1 and 6"

    data = {
        1 : [
            {
                "filter" : Q(exercise_level = "Low"),
                "ratio" : 1
            }
        ],
        2 : [
            {
                "filter" : Q(exercise_level = "Low"),
                "ratio" : 1
            }
        ],
        3 : [
            {
                "filter" : Q(exercise_level = "Low"),
                "ratio" : 0.7
            },
            {
                "filter" : Q(exercise_level = "Moderate"),
                "ratio" : 0.3
            }
        ],
        4 : [
            {
                "filter" : Q(exercise_level = "Low"),
                "ratio" : 0.5
            },
            {
                "filter" : Q(exercise_level = "Moderate"),
                "ratio" : 0.5
            }
        ],
        5 : [
            {
                "filter" : Q(exercise_level = "Low"),
                "ratio" : 0.3
            },
            {
                "filter" : Q(exercise_level = "Moderate"),
                "ratio" : 0.7
            }
        ],
        6 : [
            {
                "filter" : Q(exercise_level = "Moderate"),
                "ratio" : 1
            }
        ]
    }
    return data.get(user_week_no)
