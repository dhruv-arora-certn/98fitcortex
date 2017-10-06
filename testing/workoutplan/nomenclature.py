from django.db.models import Q

class BodyBase:

	def compound(self):
		self.filter = Q(exercise_type = "Compound") | Q(exercise_type = "compound")
		return self

	def isolated(self):
		self.filter = Q(exercise_type = "Isolated")

class _UpperBody(BodyBase):

	def __init__(self):
		self.filter = Q()
		self.baseQ = Q(body_part = "Upper")


	@property
	def chest(self):
		return self.baseQ & self.filter & Q(muscle_group_name = "Chest")

	@property
	def back(self):
		return self.baseQ & self.filter & Q(muscle_group_name = "Back")

	@property
	def back_biceps(self):
		return self.baseQ & self.filter & Q(muscle_group_name = "Back,Biceps")| Q(muscle_group_name = "Back,Biceps")

	@property
	def abdomen(self):
		return self.baseQ & self.filter & Q(muscle_group_name = "Abdominals") | Q(muscle_group_name = "Abs") | Q(muscle_group_name = "Abdomen")

	@property
	def biceps(self):
		return self.baseQ & self.filter & Q(muscle_group_name = "Biceps")

	@property
	def triceps(self):
		return self.baseQ & self.filter & Q(muscle_group_name = "Triceps")

	@property
	def shoulder(self):
		return self.baseQ & self.filter & Q(muscle_group_name = "Shoulder") | Q(muscle_group_name = "Shoulders")

	@property
	def chest_tricep(self):
		return self.baseQ & self.filter & Q(muscle_group_name = "Chest & Tricep")

	@property
	def chest_tricep_back(self):
		return self.baseQ & self.filter & Q(muscle_group_name = "Chest, Tricep & Back")


class _LowerBody(BodyBase):

	def __init__(self):
		self.baseQ = Q(body_part = "Lower")
		self.filter = Q()

	@property
	def calves(self):
		return self.baseQ & self.filter & Q(muscle_group_name = "Calves")

	@property
	def quadriceps(self):
		return self.baseQ & self.filter & Q(muscle_group_name = 'Quadriceps')

	@property
	def hamstrings(self):
		return self.baseQ & self.filter & Q(muscle_group_name__contains = "Hamstring")

	@property
	def glutes(self):
		return self.baseQ & self.filter & Q(muscle_group_name = "Glutes")

	@property
	def legs(self):
		return self.baseQ & self.filter & Q(muscle_group_name = "legs")



UpperBody = _UpperBody()
LowerBody = _LowerBody()
