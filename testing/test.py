from dietplan.goals import Goals
from dietplan.utils import annotate_food
from dietplan.models import Food
from dietplan.calculations import Calculations
from dietplan.bodyTypes import BodyTypes
from dietplan.activity import ActivityLevel
from dietplan.meals import M1 , M5 , M3
from knapsack.knapsack_dp import knapsack,display

weight = 75
height = 1.75
goal = Goals.MuscleGain
activity = ActivityLevel.sedentary
print(activity)
exclude = [ "Fruit Raita" , "Garlic Methi Khakra" , "Tea with Skimmed Milk, Without Sugar"]
c = Calculations(weight , height , activity , goal , exclude = exclude)
c.makeMeals()
# F,test = knapsack(m.marked , m.calories_remaining)
# items = [m.marked[i] for i in display(F,m.calories_remaining , m.marked)]