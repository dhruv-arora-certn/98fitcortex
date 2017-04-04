import lego
class BasalMetabolicRate:
	@lego.assemble
	def __init__(self , weight , leanFactor):
		self.bmr = self.weight * 24 * self.leanFactor