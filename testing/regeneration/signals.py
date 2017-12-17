from django.dispatch import Signal




attribute_changed = Signal(providing_args = ["attribute"])

instance_changed = Signal(providing_args=["instance"])

diet_regeneration = Signal(
	providing_args = [
		"user"
	]
)

workout_regeneration = Signal(
	providing_args = [
		"user"
	]
)
