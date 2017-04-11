from dietplan.goals import Goals
from dietplan.utils import annotate_food
from dietplan.models import Food
from dietplan.calculations import Calculations
from dietplan.bodyTypes import BodyTypes
from dietplan.activity import ActivityLevel
from dietplan.meals import M1 , M5 , M3
from dietplan.gender import Male,Female
from knapsack.knapsack_dp import knapsack,display
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

weight = 78
height = 1.75
goal = Goals.WeightLoss
activity = ActivityLevel.sedentary
gender = Male.number
print(activity)
exclude = [ "Fruit Raita" , "Garlic Methi Khakra" , "Tea with Skimmed Milk, Without Sugar"]
c = Calculations(weight , height , activity , goal , gender ,exclude = exclude)
# c.makeMeals()
# fig = plt.figure()
# ax = Axes3D(fig)
# f = list(annotate_food(Food.objects.filter(calarie__gt= 0),goal))
# ax.scatter(
# 	xs = [e.p for e in c.selected] , ys = [e.c for e in c.selected] , zs = [e.f for e in c.selected]
# 	, c = "r",
# 	marker = "^",
# 	s = [100 for _  in c.selected]
# )
# ax.plot(
# 	xs = [e.p for e in c.selected] , ys = [e.c for e in c.selected] , zs = [e.f for e in c.selected]
# 	,c = "black"
# )
# ax.scatter(
# 	xs = [e.p for e in f] , ys = [e.c for e in f] , zs = [e.f for e in f]
# 	,c = 'y'
# )


# ax.set_xlabel("Protein")
# ax.set_ylabel("Carbs")
# ax.set_zlabel("Fat")
# F,test = knapsack(m.marked , m.calories_remaining)
# items = [m.marked[i] for i in display(F,m.calories_remaining , m.marked)]