from datetime import datetime,timedelta,time

from django.db import models 
from django.db.models.expressions import RawSQL 
from django.db.models.functions import Coalesce
from django.utils.dateparse import parse_datetime

from weasyprint import HTML

from django.template.loader import render_to_string

from django.utils import timezone

from types import SimpleNamespace

import json
import datetime as dt
import itertools
import functools
import re

def get_week(date = None):
    '''
    Get ISO week number of the date
    '''
    if not date:
        date = datetime.now(tz = timezone.get_current_timezone())
    return date.isocalendar()[1]

def get_day(date = None):
    '''
    Get ISO weekday
    '''
    if not date:
        date = datetime.now(tz = timezone.get_current_timezone())
    return date.isocalendar()[2]

def get_year(date = None):
    '''
    Get ISO year
    '''
    if not date:
        date = datetime.now(tz = timezone.get_current_timezone())
    return date.isocalendar()[0]

def get_month(date = None):
    '''
    Get month of the year of the given date
    '''
    if not date:
        date = datetime.now(tz = timezone.get_current_timezone())
    return date.month

def count_weeks(start , end = None):
    '''
    Count number of weeks elapsed between the `start` and `end` date
    '''
    if not end:
        end = datetime.now(tz = timezone.get_current_timezone())
    start_year , start_week , start_day = start.isocalendar()
    end_year , end_week , end_day = end.isocalendar()

    if start_year < end_year:
        final_week = dt.date(
            year = start_year,
            month = 12,
            day = 31
        ).isocalendar()[1]

        count = final_week - start_week
        count += end_week
    else:
        count = end_week - start_week
    return count

def is_valid_week(year,week):
    '''
    Check if the the given `year` and `week` are allowed for user to view
    '''
    current_year = get_year()
    current_week = get_week()

    if year < current_year:
        count = 52 - week +  current_week
        return count <= 2
    elif year > current_year:
        count = 52 - current_week + week
        print("Count",count)
        return count <= 2
    else:
        return abs(week - current_week) <= 2

def aggregate_avg(field , qs):
    return qs.aggregate(average =  Coalesce(models.Avg(field) , 0))

def aggregate_min(field,qs):
    return qs.aggregate( minimum =  Coalesce(models.Min(field) , 0))

def aggregate_max(field,qs):
    return qs.aggregate( maximum = Coalesce(models.Max(field) , 0))

def aggregate_sum(field,qs):
    return qs.aggregate(total = Coalesce(models.Sum(field) , 0))

def previous_day():
    today = datetime.now().date()
    return today - timedelta(days = 1)

def countGlasses(queryset):
        queryset = queryset.annotate(
            glasses =models.Sum(models.Case(
                models.When(
                    container__name = "glass",
                    then = models.F("count")
                ),
                default = 0,
                output_field = models.IntegerField()
            )
        ))
        return queryset

def countBottles(queryset):
        queryset = queryset.annotate(
            bottles = models.Sum(models.Case(
                models.When(
                    container__name = "bottle",
                    then = models.F("count")
                ),
                default =0,
                output_field = models.IntegerField()
            ))
        )
        return queryset

def diabetes_pdf(cals , day):
    with open("disease-data/pdf-list.json" , "r") as f:
        a = json.load(f)
    return a.get("%s-%s"%(cals,day))

def relative_to_week(k):
    if k == 0:
        k = 52
    else :
        k = (k + 52)%52
    return k

class BulkDifferential:

    def getToDelete(self , old , new):
        old_names = [getattr(e , self.BulkMeta.attr_name) for e in old]
        new_names = [getattr(e , self.BulkMeta.attr_name) for e in new]

        common = []
        for e in old:
            if not getattr(e , self.BulkMeta.attr_name) in new_names:
                common.append(e)
        return common

    def getToAdd(self , old , new):
        old_names = [ getattr(e , self.BulkMeta.attr_name) for e in old]
        new_names = [ getattr(e , self.BulkMeta.attr_name) for e in new]

        common = []
        for e in new:
            if not getattr(e , self.BulkMeta.attr_name) in old_names:
                common.append(e)
        return common

def get_count_post_date(date , iterable , key):
    return filter(
        lambda x : getattr(x , key) > date,
        iterable
    )

def get_food_cat_diabetes(user):
    food_cat = user.food_cat
    if food_cat in ("nonveg" , "egg"):
        food_cat = "nonveg"
    return food_cat

def get_food_cat_pcod(user):
    return user.food_cat

def disease_cals(user):
    c = Calculations(*user.args_attrs)
    rounded_cals = round(c.calories/100)*100
    if rounded_cals <= 1200:
        cals = 1200
    elif rounded_cals == 1300:
        cals = 1300
    else:
        cals = 1400

def accumulate_sum(group , keyfunc = None):
    return sum(
        keyfunc(e) for e in group
    )

def seconds_to_hms(secs):
    '''
    Convert `secs` to HH:MM:SS representation
    '''
    m,s = divmod(secs , 60)
    h,m = divmod(m , 60)
    return "%d:%02d:%02d"%(h, m, s)

def last_days_filter(baseQ , days = 6):
    today_date = datetime.today().date()
    baseQ = baseQ.filter(
        date__lte = today_date,
        date__gt = today_date - timedelta(days = days)
    )
    return baseQ

def annotate_sleep_time(baseQ):
    start_cutoff = time(
        hour = 0, minute = 0, second = 0
    ) 

    when1 = models.When(
        start_time__gt = start_cutoff,
        start_time__lt = "05:00:00",
        then = RawSQL(
            "\
            DATE(\
               DATE_SUB(\
                start , interval 1 day\
               )\
            )\
            ",[]
        )
    )
    when2 = models.When(
        start_time__gt = "05:00:00",
        then = RawSQL(
            "DATE(start)",[]
        )
    )

    return baseQ.annotate(
        sleep_date = models.Case(
            when1,
            when2,
            output_field = models.DateField()
        )
    )

def check_dietplan_dependencies(user):
        '''
        Check if the dependencies for the dietplan are satisfied
        '''
        val = all(map(
            bool,
            [
                user.height,
                user.weight,
                user.activity_level_to_use(),
                user.food_cat
            ]
        ))
        return val


def get_meal_string(dietplan, meal):
    '''
    Return the meal string for a dietplan
    '''
    return

def can_log_sleep(sleep_logs, new_data):
    border_date = (parse_datetime(new_data['start']) - dt.timedelta(hours = 5)).date()
    sleep_log = sleep_logs.annotate(
    date = RawSQL(
        "DATE(DATE_SUB(start, INTERVAL 5 HOUR))",
        []
        )
    )
    sleep_log = sleep_log.filter(
        date = border_date
    )
    if sleep_log.count():
        return False
    return True

def hasFoodinMeal(meal, food_type , query):
    '''
    Check if a food_type exists in the meal
    '''
    count = query.filter(
       meal_type = meal,
       food_type = food_type
    ).count()

    return bool(count)

def hasM3Combo(day_query):
    '''
    Check if M3 has combination
    '''
    return hasFoodinMeal(
        meal = 'm3',
        food_type = 'combination',
        query = day_query
    )

def hasM5Combo(day_query):
    '''
    Check if M5 has a combination
    '''
    return hasFoodinMeal(
        meal = 'm5',
        food_type = 'combination',
        query = day_query
    )

def hasDessert(day_query):
    '''
    Check if the day has dessert in it
    '''
    count = day_query.filter(food_type = "dessert").count()
    return bool(count)

def getUserCalculationArgs(user):
    '''
    Return Dictionary containing user parameters required for dietplan calculations
    '''
    return {
        'height' : user.height,
        'weight' : user.weight,
        'activity' : float(user.activity_level_to_use()),
        'goal' : user.goal,
        'gender' : user.gender.number,
        'exclude' : [],
        'disease' : None,
        'exclusion_conditions' : user.get_exclusions(),
        'exclude2' : [],
        'comboDays' : None,
        'dessertDays' : None
    }

def accumulate_nutrition(a,b):
    '''
    Add nutrition of two items
    '''
    a.calories += float(b.calorie)
    a.protein += b.food_item.protein
    a.carbohydrates += b.food_item.carbohydrates
    a.fat += b.food_item.fat
    a.veg &= not(b.food_item.non_veg)
    return a

def add_favourites(user, day, week, year):
    '''
    Add Favourites for Day, Meals
    '''

    data = dict(favourites = dict(
        day = 0,
        m1 = 0,
        m2 = 0,
        m3 = 0,
        m4 = 0,
        m5 = 0
    ))
    customer_calendar, created = user.calendar.get_or_create(
        week = week,
        year = year
    )

    day_fav = customer_calendar.favourites.filter(
        day = day,
        type = 2
    )

    if day_fav.count():
        data['favourites'].update({
            "day" : day_fav.first().preference
        })
    
    meal_favs = customer_calendar.favourites.filter(
        day = day,
        type = 1
    ).values("meal","preference").distinct()

    vals_map = map(lambda x : x.values(), meal_favs)
    
    for i,e in vals_map:
        data['favourites'].update({
            'm%d'%i : e
        })

    return data


def get_meals_meta(meals, **kwargs):
    '''
    Get meta for meals
    '''
    initializer = SimpleNamespace(
        calories = 0,
        protein = 0,
        fat = 0,
        carbohydrates = 0,
        veg = True,
        dietplan = meals.first().dietplan.id,
        **kwargs
    )
    val = functools.reduce(accumulate_nutrition, meals, initializer)

    return val.__dict__

def check_add_meal_followed(meta, **kwargs):
    '''
    Check if the diet plan corresponding to the kwargs has been followed and add information to meta
    '''
    from epilogue.models import CustomerDietPlanFollow as model
    
    try:
        obj = model.objects.get(**kwargs)
    except  model.DoesNotExist as error:
        meta.update({
            "followed" : False
        })
    else:
        meta.update({
            "followed" : obj.followed
        })
    finally:
        return meta

def get_items_from_meals(queryset):
    '''
    Get list of food items in a meal
    '''
    return list(
        queryset.values_list("food_name" , flat = True).distinct()
    )

def get_diet_plan(user, week = get_week(), year = get_year()):
    '''
    Return the user's dietplan for the week of the year
    '''

    return user.dietplans.filter(week_id = week, year = year).last()

def get_day_items_from_dietplan(dietplan, day = None):
    '''
    Return the day items from dietplan
    '''
    
    if not day:
        day = get_day()

    from epilogue.models import GeneratedDietPlanFoodDetails

    items = GeneratedDietPlanFoodDetails.objects.filter(
        dietplan__id = dietplan.id,
        day = day
    )
    return items

@functools.lru_cache()
def get_meal_times(disease = False):
    if not disease:
        return ["m%d"%i for i in range(1,6)]

def get_meal_string_dict(meals):
    '''
    Get the dictionary containing the string of food items in meals
    '''
    meal_times = get_meal_times()
    string_dict = {
        e : ' + '.join([
            a.food_name for a in meals.filter(meal_type = e)
        ])
        for e in meal_times
    }
    return string_dict

def get_user_calendar(user, week, year):
    '''
    Return User's calendar object
    '''
    calendar, created = user.calendar.get_or_create(
        week = week,
        year = year
    ) 

def parse_height(height:str = None, height_type:int = None) -> float:
    '''
    Parses the height string and returns the height in metres.
    '''
    #Take care of the case when height is not set 
    if not height:
        return 0.0

    #Take care of the case when height is `0`
    if not float(height):
        return 0.0

    #Height is set
    #Height is ft,in
    if height_type ==  1:
        feet, inches = str(height).split(".")
        inches = 12 * float(feet) + float(inches)
        return round(inches * 0.0254,2)

    elif height_type == 2:
        return round(int((float(height)))/100,2)
    
    return 0.0

def parse_weight(weight:str = None, weight_type:int = None) -> float:
    '''
    Parse Weight string and returns weight in kgs
    '''
    if not weight:
        return 0.0

    if not float(weight):
        return 0.0
    
    #Weight is in kgs
    if weight_type == 2:
        return round(float(weight),2)
    
    #Weight is in lbs
    if weight_type == 1:
        return round(
            float(weight) * 0.4536, 2
        )

def _validate_regex(pattern:str, string:str) -> bool:
    '''
    Match the given string with regex
    '''
    if re.match(pattern, string):
        return True

    return False

def validate_height(height:str) -> bool:
    '''
    Check if the height is a valid string
    '''
    regex = r'^\d+(\.\d{1,2})?$'

    return _validate_regex(regex, height)

def validate_weight(weight:str) -> bool:
    '''
    Check if the weight is a valid string
    '''
    regex = r'^\d+(\.\d{1,2})?$'

    return _validate_regex(regex, weight)
