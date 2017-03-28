
class BMIClassificationBase:
	upper = 100
	lower = 0

	@classmethod
	def is_true(self , bmi):
		self.truth = self.lower <= bmi < self.upper 
		return self.truth

	def __str__(self):
		return self.__name__


class BMI:
	class UnderWeight(BMIClassificationBase):
		upper = 18.5

	class NormalWeight(BMIClassificationBase):
		lower = 18.5
		upper = 25

	class OverWeight(BMIClassificationBase):
		lower = 25
		upper = 30

	class Obese(BMIClassificationBase):
		lower = 30
	
	classifications = [OverWeight , NormalWeight , UnderWeight , Obese]
	
	def __init__(self , weight, height):
		self.weight = weight
		self.height = height
		self.bmi = self.weight/self.height**2
	
	@property
	def category(self):
		return [e for e in self.classifications if e.is_true(self.bmi)].pop()