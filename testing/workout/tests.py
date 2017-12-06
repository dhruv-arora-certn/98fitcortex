from django.test import TestCase

# Create your tests here.

from .persister import WorkoutWeekPersister
from epilogue.models import Customer
from workoutplan.generator import Generator


c = Customer.objects.get(pk = 8)
g = Generator(c)
g.generate()
w = WorkoutWeekPersister(g , 1)
