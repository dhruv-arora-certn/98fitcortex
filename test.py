from dietplan.goals import Goals
from dietplan.utils import annotate_food
from dietplan.models import Food
from dietplan.calculations import Calculations
from dietplan.bodyTypes import BodyTypes
from dietplan.activity import ActivityLevel
from dietplan.meals import M1 , M5 , M3
from knapsack.knapsack_dp import knapsack,display

weight = 95
height = 1.75
goal = Goals.WeightLoss
bodytype = BodyTypes.Obese
activity = ActivityLevel.moderately_active

exclude = ["Paneer Masala" , "Fruit Raita"]
c = Calculations(weight , height , bodytype , activity , goal , exclude = exclude)

# F,test = knapsack(m.marked , m.calories_remaining)
# items = [m.marked[i] for i in display(F,m.calories_remaining , m.marked)]