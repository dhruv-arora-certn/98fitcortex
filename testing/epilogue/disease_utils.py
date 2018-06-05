from dietplan import calculations

import json

DIABETES_FILE_TEMPLATE = "disease-data/diabetes-%s-%s-%s.json"
PCOD_FILE_TEMPLATE = "disease-data/pcos-%s-%s-%s.json"

def get_rounded_cals(user):
    '''
    Return rounded of calories
    '''
    c = calculations.Calculations(*user.args_attrs)
    rounded_cals = round(c.calories/100)*100

    if rounded_cals <= 1200:
        cals = 1200
    elif rounded_cals == 1300:
        cals = 1300
    else:
        cals = 1400

    return cals

def load_json(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    return data

def get_diabetes_plan(cals, food_cat, day):
    '''
    Return the diabetes plan based on calories, food category and day
    '''
    
    if food_cat == "egg":
        food_cat = "nonveg"

    file_to_read = DIABETES_FILE_TEMPLATE%(
        cals, day, food_cat
    )

    return load_json(file_to_read)

def get_diabetes_meta(user_id,cals):
    return {
        "disease" : "diabetes",
        "calories" : cals,
        "allow-replace" : False,
        "user_id" : user_id,
    }

def get_diabetes(user, day):
    cals =  get_rounded_cals(user)
    meta  = get_diabetes_meta(user.id, cals)
    meals = get_diabetes_plan( cals, user.food_cat, day)

    return {
        "meta" : meta,
        "data" : meals
    } 

def get_pcod_plan(cals, food_cat, day):
    '''
    Return the pcos plan based on calories, food category and day
    '''

    file_to_read = PCOD_FILE_TEMPLATE%(
        cals, day, food_cat
    )
    
    return load_json(file_to_read)

def get_pcod_meta(user_id, cals):
    return {
        "disease" : "pcod",
        "calories" : cals,
        "allow-replace" : False,
        "user_id" : user_id,
    }

def get_pcod(user, day):
    cals = get_rounded_cals(user)
    meta = get_pcod_meta(user.id, cals)
    meals = get_pcod_plan(cals, user.food_cat, day)

    return {
        "meta" : meta,
        "data" : meals
    }

