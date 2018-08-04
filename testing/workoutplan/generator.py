from . import levels
from .goals import Goals
from .utils import NoviceDays , BeginnerDays , IntermediateDays , days as namedDays ,  get_resistance_filter , get_category_decorator
from .day import ExerciseDay
from . import shared_globals

import random
import logging
import sys
import os
import itertools

class ResistanceDistribution:

    def __init__(self , user , day , day_number):
        self.user = user
        self.day = day
        self.day_number = day_number

class Generator():

    def __init__(self, user):
        self.logger = logging.getLogger('workoutplan.generator')
        self.user =  user
        self.conditional_days = self.get_conditional_days()
        self.get_resistance_distribution()
        self.logger.info("Starting Workout Generator for user %s-%d"%(self.user.email , self.user.id))

        setattr(shared_globals , "location_pref" , self.user.workout_location)

    @get_category_decorator(NoviceDays)
    def _get_novice_days(self):
        pass

    @get_category_decorator(BeginnerDays)
    def _get_beginner_days(self):
        pass

    @get_category_decorator(IntermediateDays)
    def _get_intermediate_days(self):
        pass

    def _get_days_distribution(self, days):
        '''
        @days is a namedtuple instance with cardio , rt and total.
        #Notes
        Ideally should be a utility function, but i realized that after writing it and as of right now, too lazy to move it out. Hence
        a classmethod
        '''
        day_range = set(range(1 , days.total + 1))

        if not any([
            days.cardio == days.total,
            days.rt == days.total,
            days.cs == days.total
        ]):
            rt_days = sorted(random.sample(
                day_range , days.rt
            ))
            cardio_days = sorted(random.sample(
                day_range.difference(rt_days) , days.cardio
            ))
            cs_days = sorted(random.sample(
                cardio_days , days.cs
            ))
            return cardio_days , rt_days , cs_days

        cardio_days = set(random.sample(
            day_range,
            days.cardio
        ))

        if days.total <= days.cardio + days.rt:
            rt_days = random.sample(day_range , days.rt)

        else:
            rt_days = random.sample(day_range.difference(cardio_days) , days.rt)

        if self.user.is_novice():
            cs_days = cardio_days

        elif self.user.is_intermediate() and self.user.goal == Goals.WeightGain:
            cs_days = random.sample( day_range , 2)

        else:
            cs_days_count = day_range.difference(rt_days)
            cs_days = random.sample(
                day_range.difference(rt_days),
                min(len(cs_days_count),2)
            )

        return cardio_days , set(rt_days) , set(cs_days)

    def get_resistance_distribution(self):
        '''
        Get days on which user has to do resistance training
        '''

        rt_days = self.conditional_days.rt
        dist = {}

        if rt_days:
            for i,e in enumerate(rt_days):
                f = get_resistance_filter(self.user , i+1)
                dist[e] = f

        self.resistance_distribution = dist
        return dist

    def get_conditional_days(self):
        '''
        Number of Cardio Days for the user
        '''
        if self.user.level_obj == levels.Novice:
            days = self._get_novice_days()
        elif self.user.level_obj == levels.Beginner:
            days = self._get_beginner_days()
        elif self.user.level_obj == levels.Intermediate:
            days = self._get_intermediate_days()
        cardio_days , rt_days , cs_days = self._get_days_distribution(days)
        data = namedDays(cardio_days , rt_days , cs_days ,days.total)
        shared_globals.conditional_days = data
        return data

    def get_resistance_filter_for_day(self , day):
        return self.resistance_distribution.get(day)

    def should_make_cardio(self , day):
        return day in self.conditional_days.cardio

    def should_make_cs(self , day):
        return day in self.conditional_days.cs

    def _generate(self):
        days = range(1 , self.conditional_days.total + 1)
        for e in days:
            resistance_filter = self.get_resistance_filter_for_day(e)
            make_cardio = self.should_make_cardio(e)
            make_cs = self.should_make_cs(e)
            if resistance_filter or make_cardio or make_cs:
                d = ExerciseDay(e , self.user , make_cardio = make_cardio , resistance_filter = resistance_filter , make_cs = make_cs)
                setattr(self , "D%s"%e , d)
                d.build()
        return self

    def weekly_as_dict(self):
        days = set(range(1 , self.conditional_days.total + 1))
        data = {}
        for d in days:
            if hasattr(self , "D%d"%d):
                data[d] = {}
                day_obj = getattr(self , "D%d"%d)
                data[d].update(
                    **day_obj.as_dict()
                )
        return data

    def generate(self ):
        self._generate()
        return self
        try:
            self._generate()
        except Exception as e:
            exc_type , exc_obj , exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.logger.info("Error Generating Workout Plan: %s %s %s"%(exc_type , fname , exc_tb.tb_lineno))
        else:
            self.logger.info("Workout Successfully Generated for user")
        return self

    def iterdays(self):
        days = range( 1 , self.conditional_days.total + 1)
        for e in days:
            day_template = "D%d"
            if hasattr(self , day_template%e):
                self.logger.debug("Yielding Day %d"%e)
                yield getattr(self , day_template%e)
