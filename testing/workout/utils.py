from workout.serializers import GeneratedExercisePlan


def get_day_from_generator(generator , day):
	return getattr(generator , "D%s"%day)

def serialize_exercise(exercise):
	pass

def serialize_day(day_obj , workoutplan_id):
	data = day_obj.as_dict()
	pass




