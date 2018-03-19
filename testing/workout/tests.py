from django.test import TestCase
from rest_framework.test import APIRequestFactory
# Create your tests here.

from .persister import WorkoutWeekPersister
from .models import ResistanceTrainingExercise
from .week_upgrade import valid_fitness, upgrade

from epilogue.models import Customer

from workoutplan.generator import Generator
from workoutplan import levels


factory = APIRequestFactory()


class WorkoutTestCase(TestCase):
	fixtures = ["fixtures/rt.json"]

	def test_count(self):
		assert ResistanceTrainingExercise.objects.count() != 0


class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

def get_custom_user(level,week):
    return type(
        "CustomerUser",
        (),
        {   
            "level_obj" : level,
            "user_relative_workout_week" : week
        }
    )()

def test_workout():
    c = Customer.objects.get(pk = 8)
    g = Generator(c)
    g.generate()

    ws = WorkoutWeekPersister(g)


def check_valid_fitness(week, correct_fitness):
    assert valid_fitness(week) == correct_fitness , "Fitness Should be %s"%(str(correct_fitness))


def test_valid_fitness():
    print(bcolors.OKBLUE + "Running Tests for Valid Fitness Tada")
    mapping = {
        ( levels.Novice , 1) : levels.Novice,
        ( levels.Novice , 2) : levels.Novice,
        ( levels.Novice , 3) : levels.Novice,
        ( levels.Novice , 4) : levels.Novice,
        ( levels.Novice , 5) : levels.Novice,
        ( levels.Novice , 6) : levels.Novice,
        ( levels.Novice , 7) : levels.Beginner,
        ( levels.Beginner , 7) : levels.Beginner,
        ( levels. Beginner , 15) : levels.Beginner,
        ( levels.Beginner , 24) : levels.Beginner,
        ( levels.Beginner , 25) : levels.Intermediate,
        ( levels.Intermediate , 25) : levels.Intermediate,
        ( levels.Intermediate , 10) : levels.Novice,
        ( levels.Intermediate , 50) : levels.Intermediate
    }

    for k,v in mapping.items():
        print(bcolors.ENDC + "="*15)
        print( bcolors.HEADER + "Testing %s , week %d"%(str(k[0]),k[1]))
        try:
            user = get_custom_user(*k)
            check_valid_fitness(k[1],v)
        except AssertionError as e:
            print(bcolors.FAIL + "Failed Test")
            print(e)
        except TypeError as te:
            print(bcolors.FAIL + "Error %s , week %d"%(str(k[0]),k[1]))
            print(bcolors + te )
        else:
            print(bcolors.OKGREEN + "Successful")

