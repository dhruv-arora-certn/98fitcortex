from django.db.models import Q

class QUtils:
	@classmethod
	def OR(self , *args):
		if args:
			query = Q()
			for e in query:
				query |= e 
			return query
		return 

	@classmethod
	def AND(self , *args):
		if args:
			query = Q()
			for e in query:
				query &= e
			return query
		return