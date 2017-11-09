from django.db.models import Q

class UpperBody:
	filter = Q(body_part = "Upper")

class LowerBody:
	filter = Q(body_part = "Lower")
