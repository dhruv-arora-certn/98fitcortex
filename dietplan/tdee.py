class TDEE:
	def __init__(self , bmr , activity):
		self.bmr = bmr
		self.activity = activity

		self.tdee = bmr * activity