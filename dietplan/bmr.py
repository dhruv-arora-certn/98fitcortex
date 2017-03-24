class BasalMetabolicRate:
	def __init__(self , weight , leanFactor):
		self.weight = weight
		self.leanFactor = leanFactor
		self.bmr = self.weight * 24 * self.leanFactor