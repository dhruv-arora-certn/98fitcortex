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
from epilogue.manipulation.manipulator import *
from dietplan.categorizer.categorizers import *
import itertools

weight = 95 
height = 1.78
goal = Goals.WeightLoss
activity = ActivityLevel.moderately_active
gender = Male.number
exclude = []

def generate_diet_plan():
	p = Pipeline(weight , height , activity , goal , gender)
	c = Calculations(weight , height , activity , goal , gender , exclude)
	return p,c

def regenerate():
	c = Customer.objects.get(pk = 8)
	g = c.dietplans.last()
	gf = GeneratedDietPlanFoodDetails.objects.filter(dietplan = g).filter(meal_type = 'm1')
	dish = gf.last()
	r = ReplacementPipeline(dish= dish , replaceMeal = True)
	return c,g,gf,dish,r

def categoriser():
	f = Food.m3_objects.filter(grains_cereals = 1)
	m = Manipulator(items = f  , categorizers= [ GrainsCerealsCategoriser ])
	l = m.categorize()
	return f,m,l

p,c = generate_diet_plan()
