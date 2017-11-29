from django.db.models import Q

class Home:
	filter = Q(home = True)

class FitnessCentre:
	filter = Q(gym = True)
