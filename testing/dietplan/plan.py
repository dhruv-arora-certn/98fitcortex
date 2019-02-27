from .models import Food
import lego

class M1:
	#l@ego.assemble.assemble
	def __init__(self , calories , protein , carbs, fat):
		pass
		
	def generate(self):
		return Food.set_context({
			'fat' : self.fat
			'protein' : self.protein,
			'carbs' : self.carbs
		}).objects(m1 = 1)

class Plan():
	def __init__(self , calculations ):
		self.calculations = calculations

	def plan_m1(self):
		self.m1 = M1(self.calculations.caloriecount() , self.calculations.goal.protein , self.calculations.goal.carbs , self.calculations.goal.fat )

