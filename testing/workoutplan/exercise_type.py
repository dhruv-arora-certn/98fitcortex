
class Base():
	
	def __init__(self):
		pass


class Warmup(Base):
	_type = "warmup"
	duration = 300

	def __init__(self , user , duration = 300 , mainExercise = None):
		self.user = user
		self.duration = duration
		self.mainExercise = mainExercise
	
	def floor_based_cardio(self):
		'''
		To be used in the case where main exercise is Floor Based Cardio
		'''
		pass
	def normal_warmup_cooldown(self):
		'''
		To be used in the case where a normal Warm Up and Cool Down is to be generated
		'''
		pass
	

class Main(Base):
	_type = "main"
	def __init__(self):
		pass

class CoolDown(Base):
	_type = "cooldown"
	def __init__(self):
		pass

class Stretching(Base):
	_type = "stretching"
	def __init__(self):
		pass
