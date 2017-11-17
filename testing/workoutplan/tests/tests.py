import pytest
import functools

from .fixtures import workout
from django.core.cache import cache

def get_low_intensity_workouts(workouts):
	return filter(
		lambda x : x.exercise_level.strip().lower() == "low",
		workouts
	)

def get_moderate_intensity_workouts(workouts):
	return filter(
		lambda x : x.exercise_level.strip().lower() == "moderate",
		workouts
	)


def test_total_warmup_duration(workout):
	for i,e in workout.items():
		duration = sum(obj.duration for obj in e['warmup'])
		assert duration == 300 , "Warmup Duration is not 300 on Day %d"%i

def test_beginner_warmup_duration(workout):

	for i,e in workout.items():
		low_intensity_warmup = get_low_intensity_workouts(e['warmup'])
		moderate_intensity_warmup = get_moderate_intensity_workouts(e['warmup'])

		low_intensity_duration = sum(obj.duration for obj in low_intensity_warmup)
		moderate_intensity_duration = sum(obj.duration for obj in moderate_intensity_warmup)

		assert low_intensity_duration == moderate_intensity_duration , "Warmup Duration mismatch for day:%d | slow : %d | moderate : %d"%(i , low_intensity_duration , moderate_intensity_duration)

def test_cardio_weightloss_days(workout):

	total_days = len(workout.keys())
	cardio_days = functools.reduce(
			lambda val , item : val + 1 if item.get('cardio') else val,
			workout.values(),
			0
		)
	rt_days = functools.reduce(
			lambda val , item : val + 1 if item.get('resistance_training') else val,
			workout.values(),
			0
		)

	assert total_days == 5 , "Workout should be suggested for 5 days"
	assert cardio_days == total_days , "For Beginner with Goal Weight Loss , Cardio should be built for 5 days"
	assert rt_days ==  2

def test_weightloss_cardio_duration(workout):
	for k,v in workout.items():
		duration = sum(e.duration*e.sets for e in v['cardio'])
		assert duration == 1500 , "Beginner WeightLoss Cardio to be suggested for 25 minutes"


def test_static_stretching_individual_exercise_duration(workout):
	for k,v in workout.items():
		assert all(e.duration == 15 for e in v['stretching']) , "All exercises are not of 15 seconds"
