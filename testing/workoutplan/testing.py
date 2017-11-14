from workoutplan import levels
from workoutplan import goals



def dummy_customer(level , goal , user_workout_week):
	return type(
		"DummyCustomer",
		(),
		{
			"level_obj" : level,
			"goal" : goal,
			"user_workout_week" : user_workout_week
		}
	)
