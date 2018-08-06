from . import exercise_type
from . import exercise
from . import shared_globals

from django.db.models import Q
from .utils import DummyCoolDown

class ExerciseDay:
    '''
    Generate a Day's Workout plan

    Parameters
    ----------
    `day` : int
            The of the week for which plan has to be generated
    `user` : `epilogue.models.Customer`
    `make_cardio` : bool
            Boolean indicating if cardio should be made in the day
    `make_cs` : bool
            Boolean indication if core strengthening should be made in the day
    `resistance_filter` : `django.db.models.Q`
            Filter object for resistance filters used to make Resistance Training`

    Notes
    -----
    This class is only responsible for generating a day's workout plan.
    It generates the exercises based on the parameters passed
    '''
    def __init__(self , day , user ,make_cardio = False , make_cs = False,resistance_filter = Q()):
        self.day = day
        self.make_cardio = make_cardio
        self.make_cs = make_cs
        self.make_rt = bool(resistance_filter)
        self.resistance_filter = resistance_filter
        self.user = user

    def __str__(self):
        return "Day %s"%self.day

    def __repr__(self):
        return self.__str__()

    def generate(self):
        self.buildMain(self)

    def buildMain(self):
        '''
        Generate
        - Resistance Training
        - Cardio
        - Core Strengthening 
        parts of the workout
        '''
        self.main = exercise_type.Main(self.user ,resistance_filter =  self.resistance_filter , make_cardio = self.make_cardio , make_cs = self.make_cs)
        self.main.build()

    def buildWarmup(self):
        '''
        Generate Warmup
        '''
        self.warmup = exercise_type.Warmup(self.user , mainCardio = self.main )
        self.warmup.build()
        return self

    def buildCoolDown(self):
        '''
        Generate Cooldown
        '''

        #Cooldown is built like warmup
        self.cooldown = exercise_type.Warmup(self.user , mainCardio = self.main)
        self.cooldown.build()

        self.cooldown.selected['cooldown'] = self.cooldown.selected['warmup']
        del self.cooldown.selected['warmup']

        if self.resistance_filter:
            self.cooldown.selected['cooldown'].append(
                DummyCoolDown(300 , "Slow Walk")
            )
        return self

    def buildStretching(self):
        '''
        Generate Stretching
        '''
        class Stretching:
            selected = {"stretching" : []}

        self.stretching = Stretching()

        if self.resistance_filter:
            self.rt_stretching = exercise_type.Stretching( self.user , resistance_filter = self.resistance_filter)
            self.rt_stretching.build()
            self.stretching.selected.get('stretching').extend(self.rt_stretching.selected.get("stretching"))

        if self.make_cardio:
            self.cardio_stretching = exercise_type.Stretching(self.user , cardio = True)
            self.cardio_stretching.build()
            self.stretching.selected.get('stretching').extend(self.cardio_stretching.selected.get("stretching"))

    def build(self):
        '''
        Entrypoint function for generating the day's workout
        '''
        shared_globals.day_in_progress = self.day
        self.buildMain()
        self.buildWarmup()
        self.buildStretching()
        self.buildCoolDown()
        return self

    def iterexercises(self):
        '''
        Iterate Day's exercises
        '''
        data = self.as_dict()

        for i,e in data.items():
            yield i,e

    def as_dict(self):
        '''
        Return the selected exercises as a dictionary
        '''
        return {
            **self.warmup.selected,
            **self.main.selected,
            **self.stretching.selected,
            **self.cooldown.selected
        }
