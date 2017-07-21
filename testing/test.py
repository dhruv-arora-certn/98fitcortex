from dietplan.goals import Goals
from dietplan.utils import annotate_food
from epilogue.models import *
from dietplan.calculations import Calculations
from dietplan.bodyTypes import BodyTypes
from dietplan.activity import ActivityLevel
from dietplan.meals import M1 , M5 , M3
from dietplan.gender import Male,Female
from dietplan.generator import Pipeline
from dietplan.medical_conditions import Osteoporosis , Anemia
from knapsack.knapsack_dp import knapsack,display
from epilogue.replacement import *

weight = 46 
height = 1.6
goal = Goals.WeightGain
activity = ActivityLevel.sedentary
gender = Female.number
exclude = []
p = Pipeline(weight , height , activity , goal , gender , disease = Anemia)
c = Calculations(weight , height , activity , goal , gender , exclude)

c = Customer.objects.get(pk = 8)
g = c.dietplans.last()
gf = GeneratedDietPlanFoodDetails.objects.filter(dietplan = g).filter(meal_type = 'm1')
dish = gf.last()
r = ReplacementPipeline(dish= dish , replaceMeal = True)