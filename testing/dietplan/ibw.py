import lego
class IBW:
	@lego.assemble
	def __init__(self , height):
		self.ibw = (self.height*100 - 100)*0.9