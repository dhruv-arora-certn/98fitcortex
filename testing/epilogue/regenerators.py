from . import models
from . import utils
from . import mappers

from dietplan import calculations
from dietplan import generator

from django.db.models import Q

import types

class DayRegenator:

    def __init__(self, user, day, week, year):
        self.user = user
        self.day = day
        self.week = week
        self.year = year

        self.exclusion_conditions = self.user.get_exclusions()
        
        self.dietplan = self.user.dietplans.get(
            customer = user,
            week_id = week,
            year = year
        )
        self._original_day = models.GeneratedDietPlanFoodDetails.objects.filter(
            day = day,
            dietplan__week_id = week,
            dietplan__year = year,
            dietplan__id = self.dietplan.id
        )
        self.original_day = types.SimpleNamespace(
            item_ids = list(self._original_day.values_list("id", flat = True)),
            combos = {
                'm3' : utils.hasM3Combo(self._original_day),
                'm5' : utils.hasM5Combo(self._original_day)
            },
            item_names = list(self._original_day.values_list("food_name", flat = True)),
            items = list(self._original_day.all()),
            dessert = utils.hasDessert(self._original_day)
        )
    def get_previous_day(self):
        '''
        Return the parameters of the previous day of the diet
        '''
        if self.day == 1:
            return {
                "day" : 7, 
                "dietplan__week_id" : self.week-1, 
                "dietplan__year" : self.year 
            }
        return {
            "day" : self.day - 1,
            "dietplan__week_id" : self.week,
            "dietplan__year" : self.year
        }

    def get_next_day(self):
        '''
        Return the parameters for the next day
        '''
        if self.day == 7:
            return {
                "day" : 1,
                "dietplan__week_id" : self.week + 1,
                "dietplan__year" : self.year
            }
        return {
            "day" : self.day +1,
            "dietplan__week_id" : self.week,
            "dietplan__year" : self.year
        }

    def get_excluded_items(self):
        '''
        Get list of items that should be excluded.
        Day Range : 1 
        ''' 
        previous_day = models.GeneratedDietPlanFoodDetails.objects.filter(
            **self.get_previous_day(),
            dietplan__id = self.dietplan.id
        )
        next_day = models.GeneratedDietPlanFoodDetails.objects.filter(
            **self.get_next_day(),
            dietplan__id = self.dietplan.id
        )
        qs = previous_day | next_day
        return list(qs.values_list("food_name" , flat = True).distinct())

    def make_day(self):
        '''
        Generate the Day object from passed parameters
        '''
        self.make_calculations()
        day = generator.Day(
            self.calc,
            persist = True,
            dietplan = self.dietplan,
            day = self.day
        )
        self.day_obj = day
        return self
    
    def get_user_calculation_args(self):
        '''
        Get user's calculation arguments and modify the attributes
        '''
        args = utils.getUserCalculationArgs(self.user)
        args['comboDays'] = self.original_day.combos 
        args['dessertDays'] = self.original_day.dessert
        args['exclusion_conditions'] = self.exclusion_conditions
        return args

    def make_calculations(self):
        '''
        Generate the calculations object for the day
        '''
        args = self.get_user_calculation_args()
        args['exclude'] = self.get_excluded_items()
        calc = calculations.Calculations(
           **args 
        )
        self.calc = calc
        return self 
    
    def generate(self):
        '''
        Generate the plan
        '''
        self.day_obj.makeMeals()
        return self

    def add_exclusion_condition(self, condition):
        '''
        Add a exclusion condition to the generator. All the conditions must
        be added before the calculations object is called
        '''
        
        self.exclusion_conditions &= condition
        return self

    def persist(self):
        '''
        Delegate the Day object to persist the plan
        '''
        self.day_obj.persist_db()
        return self
    
    def delete_old(self):
        self._deleted = self._original_day.filter(id__in = self.original_day.item_ids).delete()
        return self

    def regenerate(self):
        '''
        Regenerate the Day's Plan
        '''
        self.make_calculations().make_day().generate().delete_old()
        return self
    
    @property
    def new(self):
        return self.day_obj.calculations._selected

class VegRegenerator(DayRegenator):
    '''
    Regenerate the Day's plan as vegetaria
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_exclusion_condition(
            mappers.food_category_exclusion_mapper['veg']
        )
