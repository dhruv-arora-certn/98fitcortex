from types import SimpleNamespace

import functools

def as_simplenamespace(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        data = f(*args, **kwargs)
        return SimpleNamespace(**data)
    return wrapper

@functools.lru_cache()
def get_meal_repr(meal):
    return int(meal[1])

def get_item_favourite_details(item, calendar, preference):
    '''
    Return the details required to favourite an item
    - day
    - week
    - year
    - meal
    - food

    item is an instance of epilogue.GeneratedDietPlanFoodDetails
    '''
    return [
        dict(
            type = 0,
            customer_calendar = calendar.pk,
            food = item.food_item.id,
            day = item.day,
            meal = get_meal_repr(item.meal_type),
            preference = preference
        )]
 

def get_meal_favourite_details(qs, calendar, preference):
    '''
    data: instance of request.data

    Return the details required to favorite a day 
    '''
    
    #Convert the request.data dict to SimpleNamespace
    items = qs  
    return [ dict(
        type = 1,
        day = data.day,
        food = data.food_item.pk,
        meal = get_meal_repr(data.meal_type),
        preference = preference,
        customer_calendar = calendar.pk
        
    ) for data in qs]


def get_day_favourite_details(qs, calendar, preference):
    items = qs
    default_dict = functools.partial(
        dict, customer_calendar = calendar.pk, preference = preference
    )
    return [
        default_dict(
            type = 2,
            day = data.day,
            food = data.food_item.pk,
            meal = get_meal_repr(data.meal_type),
        )
        for data in qs
    ]
