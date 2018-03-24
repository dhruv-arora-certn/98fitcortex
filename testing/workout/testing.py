from epilogue.models import Customer
from workout.utils import workout_regenerator


def get_customer():
    return Customer.objects.get(pk = 8)

def regenerate_workout():
    c = get_customer()
    w = c.workouts.last()
    new_workout = workout_regenerator(w)
    return new_workout

