from . import bmi
from .BodyTypes import *

class LeanFactor:

	def __init__(self , bodyType , bmiType):
		self.bodyType = bodyType
		self.bmiType = bmiType

	def get_lean(self):
		if self.bodyType == BodyTypes.Toned:
			if self.bmiType == bmi.UnderWeight : return 1.0
			if self.bmiType == bmi.NormalWeight : return 1.0
			if self.bmiType == bmi.OverWeight : return  1.0
			if self.bmiType == bmi.Obese : return 1.0
		if self.bodyType == BodyTypes.Average:
			if self.bmiType == bmi.UnderWeight : return 1.0
			if self.bmiType == bmi.NormalWeight : return 1.0
			if self.bmiType == bmi.OverWeight : return 0.95
			if self.bmiType == bmi.Obese : return 0.85
		if self.bodyType == BodyTypes.OverWeight:
			if self.bmiType == bmi.UnderWeight : return 1.0
			if self.bmiType == bmi.NormalWeight : return 0.95
			if self.bmiType == bmi.OverWeight : return 0.90
			if self.bmiType == bmi.Obese : return 0.85
		if self.bodyType == BodyTypes.Obese:
			if self.bmiType == bmi.UnderWeight : return 1.0
			if self.bmiType == bmi.NormalWeight : return 0.90
			if self.bmiType == bmi.OverWeight : return 0.85
			if self.bmiType == bmi.Obese : return 0.85