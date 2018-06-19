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

    meal = get_meal_repr(item.meal_type)
    food = item.food_item

    return dict(
        type = 0,
        day = day,
        week = week,
        year = year,
        meal = meal,
        foods = [food.pk]
    )
 
