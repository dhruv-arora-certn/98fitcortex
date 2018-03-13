from .data import *
import itertools


def test_peridized():
    activities = [
        ActivityLevel.sedentary,
        ActivityLevel.lightly_active,
        ActivityLevel.moderately_active,
        ActivityLevel.extra_active
    ]
    fitnesses = [
        levels.Novice,
        levels.Beginner,
        levels.Intermediate
    ]
    pairs = itertools.product(fitnesses,activities)

    for f,a in pairs:
        if (a,f) in periodization_map:
            print(is_periodized(f,a))
            assert is_periodized(f,a) == True , "%s, %s  Should be periodized"%(f,a)
