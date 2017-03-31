class CalorieNumber:
	def __init__(self , bmi , activity):
		self.number = bmi.category.number(activity)