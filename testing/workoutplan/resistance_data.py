from collections import namedtuple
from .nomenclature import UpperBody , LowerBody
day = namedtuple("Day" , ["number" , "filter"])

class Day(namedtuple("Day" , ["d"+str(e) for e in range(1,8)])):
	def __new__(cls , *args , **kwargs):
		print(*args)
		print(kwargs)
		d = kwargs.pop('day')
		return super().__new__(cls , str(d))

class Novice:
	class WeightGain:
		class D1:
			filter = UpperBody.compound().baseQ | LowerBody.compound().baseQ
			count = 5

		class D2:
			pass
