import lego
class IBW:
	@lego.assemble
	def __init__(self , height , gender):
		self.ibw = (self.height*100 - 100)*self.gender