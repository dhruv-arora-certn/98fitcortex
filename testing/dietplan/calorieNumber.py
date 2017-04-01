import ipdb

class CalorieNumber:
	def __init__(self , bmi , activity):
		print("From CN activbie" , activity)
		# ipdb.set_trace()
		self.number = bmi.category.number(activity)