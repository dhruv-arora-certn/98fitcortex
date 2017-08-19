
class AggregatedData:
	def __init__(self ,*args , **kwargs):
		self.minimum = kwargs.pop("minimum")
		self.maximum = kwargs.pop("maximum")
		self.average = kwargs.pop("average")

class Weekly:
	def __init__(self , *args , **kwargs):
		print("From Weekly ," , args ,kwargs)
		self.day = kwargs.pop("day")
		super().__init__(*args , **kwargs)

class Monthly:
	def __init__(self , *args , **kwargs): 
		print("From Monthly ," , args ,kwargs)
		self.week = kwargs.pop("week") 
		super().__init__(*args , **kwargs)

class Sleep:
	def __init__(self , *args , **kwargs):
		print("From Sleep ," , args ,kwargs)
		self.minutes = kwargs.pop("minutes")
		super().__init__(*args , **kwargs)

class SleepWeekly(Weekly , Sleep):
	def __init__(self , *args , **kwargs):
		print("From SleepWeekly ," , args ,kwargs)
		super().__init__(*args , **kwargs)

class SleepMonthly(Monthly , Sleep):
	def __init__(self , *args , **kwargs):
		print("From SleepMonthly ," , args ,kwargs)
		super().__init__(*args , **kwargs)

class SleepAggregated(AggregatedData):
	def __init__(self,*args, **kwargs):
		super().__init(*args, **kwargs)
		self.minutes = kwargs.pop('minutes')
