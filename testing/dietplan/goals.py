class Base():
	@classmethod
	def get_attributes(self):
		return [self.protein , self.carbs , self.fat]

class Goals:
	
	class WeightLoss(Base):
		_diff = -0.15
		protein = 0.20
		fat = 0.25
		carbs = 0.55

		def __str__(self):
			return "Weight Loss"

	class WeightGain(Base):
		_diff = 0.10
		protein = 0.15
		fat = 0.30
		carbs = 0.55

	class MuscleGain(Base):
		_diff = 0.10
		protein = 0.25
		fat = 0.25
		carbs = 0.50
		
	class MaintainWeight(Base):
		_diff = 0
		protein = 0.15
		fat = 0.25
		carbs = 0.60