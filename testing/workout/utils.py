from workout.serializers import GeneratedExercisePlan
from workout.persister import WorkoutWeekPersister

from workoutplan.generator import Generator
from workoutplan import levels

import random
import logging


def get_day_from_generator(generator , day):
	return getattr(generator , "D%s"%day)

def serialize_exercise(exercise):
	pass

def serialize_day(day_obj , workoutplan_id):
	data = day_obj.as_dict()
	pass

class MockCustomerLevel:

    def is_novice(self):
        return  self.level_obj == levels.Novice

    def is_beginner(self):
        return self.level_obj == levels.Beginner

    def is_intermediate(self):
        return self.level_obj == levels.Intermediate

def dummy_customer(level = None , goal = None , week = None , location = None , email = None):
    return type(
        "DummyCustomer",
        (MockCustomerLevel,),
        {
            "level_obj" : level,
            "goal" : goal,
            "user_relative_workout_week" : week,
            "id" : random.randint(9,100),
            "email" : email or "test@98fit.com",
            "workout_location" : location

        }
    )()

def make_dummy_customer_like(customer , week = None , email = None):
    return dummy_customer(
        level = customer.level_obj,
        goal = customer.goal,
        week = week or customer.user_relative_workout_week,
        location = customer.workout_location 
    )

def workout_regenerator(workout):
    dummy_customer = make_dummy_customer_like(
        workout.customer,
        week = workout.user_week_id
    ) 
     
    logger = logging.getLogger("regeneration")
    logger.debug("Entering Workout Regeneration")
    #Generate New Workout
    try:
        logger.debug("Trying to regenerate workout")
        generator = Generator(
            dummy_customer        
        )
        workout_persister = WorkoutWeekPersister(
            generator,
            workout.user_week_id
        )
        workout_persister.persist()
    except Exception as e:
        logger.debug("Unable to regenerate WP")
        logger.debug(e)
        status = False
        raise 
    else:
        #NO exception was raised
        #New plan was successfully generated and persisted
        #Can Safely delete the existing plan
        logger.debug("Successful Regeneration")
        logger.debug("Old Id : %d"%workout.id)
        import ipdb
        #ipdb.set_trace()
        workout.delete()
        workout = workout_persister.model_obj
        print("New Id :%d"%workout.id)
        status = True
    finally:
        return workout , status
