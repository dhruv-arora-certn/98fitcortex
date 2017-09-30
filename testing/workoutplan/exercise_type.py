from workoutplan import exercise
from workoutplan import utils
from workout.models import FloorBasedCardio
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
	
	def decideWarmup(self):
		'''
		Decide Which Function is to be called For generating the Warmup
		The function is assigned to the object rather than returned,
		Self is returned instead
		This will enable me to perform chaining and allow subsequent functions to use the attribute
		'''
		if isinstance(self.mainExercise , exercise.FloorBasedCardio):
			self.__funcToCall = self.floor_based_cardio	
		return self

	def floor_based_cardio(self):
		'''
		To be used in the case where main exercise is Floor Based Cardio
		'''
		self.normal_warmup_cooldown()

	def normal_warmup_cooldown(self):
		'''
		To be used in the case where a normal Warm Up and Cool Down is to be generated
		'''
		pass

	def time_based_cardio(self):
		pass


class Main(Base):
	_type = "main"
	
	def __init__(self , user , makeCardio = False , makeCoreStrengthening = True , cardioDays = [] , rtDays = []):
		self.user = user
		self.makeCardio = makeCardio
		self.makeCoreStrengthening = makeCoreStrengthening
		self.cardioDays = cardioDays
		self.rtDays = rtDays

	def buildCardio(self):
		duration = 900
		#Queries
		return  
class CoolDown(Base):
	_type = "cooldown"
	def __init__(self):
		pass

class Stretching(Base):
	_type = "stretching"
	def __init__(self):
		pass
