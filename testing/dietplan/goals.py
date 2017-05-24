class Base():
	@classmethod
	def get_attributes(self):
		return [self.protein , self.carbs , self.fat , self.field]

class Goals:
	
	class WeightLoss(Base):
		_diff = -0.15
		protein = 0.20
		fat = 0.25
		carbs = 0.55
		field = "squared_diff_weight_loss"
		
		def __str__(self):
			return "Weight Loss"

	class WeightGain(Base):
		_diff = 0.10
		protein = 0.15
		fat = 0.30
		carbs = 0.55
		field = "squared_diff_weight_gain"

	class MuscleGain(Base):
		_diff = 0.10
		protein = 0.25
		fat = 0.25
		carbs = 0.50
		field = "squared_diff_weight_gain"

	class MaintainWeight(Base):
		_diff = 0
		protein = 0.15
		fat = 0.25
		carbs = 0.60
		field = "squared_diff_weight_maintain"