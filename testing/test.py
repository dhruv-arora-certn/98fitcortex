from dietplan.goals import Goals
from dietplan.utils import annotate_food
from epilogue.models import Food
from dietplan.calculations import Calculations
from dietplan.bodyTypes import BodyTypes
from dietplan.activity import ActivityLevel
from dietplan.meals import M1 , M5 , M3
from dietplan.gender import Male,Female
from dietplan.generator import Pipeline
from dietplan.medical_conditions import Osteoporosis
from knapsack.knapsack_dp import knapsack,display


weight = 46 
height = 1.6
goal = Goals.WeightGain
activity = ActivityLevel.sedentary
gender = Female.number
exclude = []
p = Pipeline(weight , height , activity , goal , gender , disease = Osteoporosis)
c = Calculations(weight , height , activity , goal , gender , exclude)