from .bmi import BMI
from .bodyTypes import *
import lego

class LeanFactor:
	#l@ego.assemble.assemble
	def __init__(self , bodyType , bmiType):
		pass

	def get_lean(self):
		if self.bodyType == BodyTypes.Toned:
			if self.bmiType == BMI.UnderWeight : return 1.0
			if self.bmiType == BMI.NormalWeight : return 1.0
			if self.bmiType == BMI.OverWeight : return  1.0
			if self.bmiType == BMI.Obese : return 1.0
		if self.bodyType == BodyTypes.Average:
			if self.bmiType == BMI.UnderWeight : return 1.0
			if self.bmiType == BMI.NormalWeight : return 1.0
			if self.bmiType == BMI.OverWeight : return 0.95
			if self.bmiType == BMI.Obese : return 0.85
		if self.bodyType == BodyTypes.OverWeight:
			if self.bmiType == BMI.UnderWeight : return 1.0
			if self.bmiType == BMI.NormalWeight : return 0.95
			if self.bmiType == BMI.OverWeight : return 0.90
			if self.bmiType == BMI.Obese : return 0.85
		if self.bodyType == BodyTypes.Obese:
			if self.bmiType == BMI.UnderWeight : return 1.0
			if self.bmiType == BMI.NormalWeight : return 0.90
			if self.bmiType == BMI.OverWeight : return 0.85
			if self.bmiType == BMI.Obese : return 0.85