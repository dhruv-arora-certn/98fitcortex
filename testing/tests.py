import pytest
from django.core.cache import cache



def get_generated_workout():
	return cache.get("workout_8_45")

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

def test_beginner_warmup_duration():
	workout = get_generated_workout()

	day1 = workout[1]
	low_intensity_warmup = get_low_intensity_workouts(day1['warmup'])
	moderate_intensity_warmup = get_moderate_intensity_workouts(day1['warmup'])

	low_intensity_duration = sum(e.duration for e in low_intensity_warmup)
	moderate_intensity_duration = sum(e.duration for e in moderate_intensity_warmup)
	
	assert low_intensity_duration == moderate_intensity_duration , "Duration mismatch low : %d | moderate : %d"%(low_intensity_duration , moderate_intensity_duration)
