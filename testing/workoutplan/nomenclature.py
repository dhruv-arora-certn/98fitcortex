from django.db.models import Q

class BodyBase:

	@classmethod
	def compound(self):
		self.filter = Q(exercise_type = "Compound") | Q(exercise_type = "compound")
		return self

	@classmethod
	def isolated(self):
		self.filter = Q(exercise_type = "Isolated")
		return self

class UpperBody(BodyBase):

	filter = Q()
	baseQ = Q(body_part = "Upper")

	@classmethod
	def groups(self):
		return  [
		(self.chest,2),
		(self.back,2),
		(self.abdomen,1),
		(self.biceps,1),
		(self.triceps,1),
		(self.shoulder,1)
	]
	@classmethod
	def chest(self):
		return self.baseQ & self.filter & Q(muscle_group_name = "Chest")

	@classmethod
	def back(self):
		return self.baseQ & self.filter & Q(muscle_group_name = "Back")

	@classmethod
	def back_biceps(self):
		return self.baseQ & self.filter & Q(muscle_group_name = "Back,Biceps")| Q(muscle_group_name = "Back,Biceps")

	@classmethod
	def abdomen(self):
		return self.baseQ & self.filter & Q(muscle_group_name = "Abdominals") | Q(muscle_group_name = "Abs") | Q(muscle_group_name = "Abdomen")

	@classmethod
	def biceps(self):
		return self.baseQ & self.filter & Q(muscle_group_name = "Biceps")

	@classmethod
	def triceps(self):
		return self.baseQ & self.filter & Q(muscle_group_name = "Triceps")

	@classmethod
	def shoulder(self):
		return self.baseQ & self.filter & Q(muscle_group_name__icontains = "shoulder") 

	@classmethod
	def chest_tricep(self):
		return self.baseQ & self.filter & Q(muscle_group_name = "Chest & Tricep")

	@classmethod
	def chest_tricep_back(self):
		return self.baseQ & self.filter & Q(muscle_group_name = "Chest, Tricep & Back")


class LowerBody(BodyBase):

	baseQ = Q(body_part = "Lower")
	filter = Q()

	@classmethod
	def groups(self):
		l = self()
		return [
			(l.compound().calves() , 1),
			(l.quadriceps(),1),
			(l.hamstrings() ,1),
			(l.glutes() , 1),
			(l.calves() ,1),
			(l.isolated().calves() , 1),
			(l.quadriceps(),1),
			(l.hamstrings() ,1),
			(l.glutes() , 1),
			(l.calves() ,1),
		]
	@classmethod
	def calves(self):
		return self.baseQ & self.filter & Q(muscle_group_name = "Calves")

	@classmethod
	def quadriceps(self):
		return self.baseQ & self.filter & Q(muscle_group_name = 'Quadriceps')

	@classmethod
	def hamstrings(self):
		return self.baseQ & self.filter & Q(muscle_group_name__contains = "Hamstring")

	@classmethod
	def glutes(self):
		return self.baseQ & self.filter & Q(muscle_group_name = "Glutes")

	@classmethod
	def legs(self):
		return self.baseQ & self.filter & Q(muscle_group_name = "legs")

