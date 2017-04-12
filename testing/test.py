from dietplan.goals import Goals
from dietplan.utils import annotate_food
from dietplan.models import Food
from dietplan.calculations import Calculations
from dietplan.bodyTypes import BodyTypes
from dietplan.activity import ActivityLevel
from dietplan.meals import M1 , M5 , M3
from dietplan.gender import Male,Female
from dietplan.generator import Pipeline
from knapsack.knapsack_dp import knapsack,display

weight = 78
height = 1.75
goal = Goals.WeightLoss
activity = ActivityLevel.sedentary
gender = Male.number
print(activity)
exclude = []
p = Pipeline(weight , height , activity , goal , gender)