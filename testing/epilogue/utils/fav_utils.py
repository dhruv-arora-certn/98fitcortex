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

@as_simplenamespace
def get_item_favourite_details(item):
    '''
    Return the details required to favourite an item
    - day
    - week
    - year
    - meal
    - food

    item is an instance of epilogue.GeneratedDietPlanFoodDetails
    '''
    day = item.day
    week = item.dietplan.week_id
    year = item.dietplan.year

    return dict(
        type = 0,
        day = day,
        week = week,
        year = year,
        foods = [{
            "food" : item.food_item.pk,
            "meal" : get_meal_repr(item.meal_type)
        } for f in [item]]
    )
 

@as_simplenamespace
def get_day_favourite_details(data):
    '''
    data: instance of request.data

    Return the details required to favorite a day 
    '''
    
    #Convert the request.data dict to SimpleNamespace
    data = SimpleNamespace(**data)
    
    return dict(
        day = data.day,
        week = data.week,
        year = data.year,
        
    )
