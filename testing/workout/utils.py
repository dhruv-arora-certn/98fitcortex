from workout.serializers import GeneratedExercisePlan
from workout.persister import WorkoutWeekPersister

from workoutplan.generator import Generator
from workoutplan import levels
from workoutplan.exercise_workout_relation import data


import random
import logging
import isoweek


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

def dummy_customer(level = None , goal = None , week = None , location = None , email = None, current_level = 1 , new_latest_activity = None):
    return type(
        "DummyCustomer",
        (MockCustomerLevel,),
        {
            "level_obj" : level,
            "goal" : goal,
            "user_relative_workout_week" : week,
            "id" : random.randint(9,100),
            "email" : email or "test@98fit.com",
            "workout_location" : location,
            "current_level" : current_level,
            "new_latest_activity" : new_latest_activity
        }
    )()

def make_dummy_customer_like(customer , week = None , email = None):
    return dummy_customer(
        current_level = customer.current_level,
        level = customer.level_obj,
        goal = customer.goal,
        week = week or customer.user_relative_workout_week,
        location = customer.workout_location,
        new_latest_activity = customer.new_latest_activity
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
        ).generate()
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
        workout.delete()
        workout = workout_persister.model_obj
        print("New Id :%d"%workout.id)
        status = True
    finally:
        return workout , status


def get_weeks_since(request,**kwargs):
    week = int(kwargs.get('week_id'))
    year = int(kwargs.get('year'))
    end = isoweek.Week(year,week).monday()
    start = request.user.get_last_level_day()

    from epilogue.utils import count_weeks
    weeks_since = count_weeks(start , end) 

    if weeks_since == 0:
        return 1

    return weeks_since + 1

def check_and_update_fitness(request , *args, **kwargs):
    '''
    Check if the fitness needs to be updated for the workout week requested
    '''
    weeks_since = get_weeks_since(request,**kwargs)
    request.user.user_relative_workout_week = weeks_since
    request.user.update_fitness(weeks_since , context = {
        "week" : int(kwargs.get("week_id")),
        "year" : int(kwargs.get("year"))
    })
    request.user.user_relative_workout_week = get_weeks_since(request,**kwargs)
    return 

def check_and_update_activity_level(request, *args, override= False , **kwargs):
    '''
    Update User's activity level 
    Either when a workout plan has been created or override signal is passed
    override signal is passed by workout view
    '''
    weeks_since = get_weeks_since(request,**kwargs)
    if not getattr(request.user,"user_relative_workout_week",None):
        request.user.user_relative_workout_week = weeks_since
    condition = request.user.workouts.count() or override
    if not condition:
        return
    logger = logging.getLogger("activity_upgrade")
    logger.debug("Calling Update Acitvity")
    data.upgrade_user(request.user, weeks_since , context = {
        "week" : int(kwargs.get("week_id")),
        "year" : int(kwargs.get("year"))
    })
    return

def set_user_level(request,*args, **kwargs):
    week = int(kwargs.get("week_id"))
    year = int(kwargs.get("year"))
    request.user.level_obj = request.user.fitness_level_to_use_obj(week = week, year = year)
