from django.dispatch import Signal




attribute_changed = Signal(providing_args = ["attribute"])

regeneration = Signal(
	providing_args = [
		"year","week"
	]
)
