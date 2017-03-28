from dietplan.goals import Goals
from dietplan.utils import annotate_food
from dietplan.models import Food
from dietplan.calculations import Calculations
from dietplan.bodyTypes import BodyTypes
from dietplan.activity import ActivityLevel
from dietplan.meals import M1

weight = 95
height = 1.7
goal = Goals.WeightLoss
bodytype = BodyTypes.OverWeight
activity = ActivityLevel.moderately_active

c = Calculations(weight , height , bodytype , activity , goal)

m = M1(c.calories , goal)
