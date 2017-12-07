from django.test import TestCase
from rest_framework.test import APIRequestFactory
# Create your tests here.

from .persister import WorkoutWeekPersister
from .models import ResistanceTrainingExercise

from epilogue.models import Customer

from workoutplan.generator import Generator


factory = APIRequestFactory()


class WorkoutTestCase(TestCase):
	fixtures = ["fixtures/rt.json"]

	def test_count(self):
		assert ResistanceTrainingExercise.objects.count() != 0
