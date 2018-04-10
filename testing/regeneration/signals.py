from django.dispatch import Signal
from django.dispatch import receiver




attribute_changed = Signal(providing_args = ["attribute"])

instance_changed = Signal(providing_args=["instance"])

diet_regeneration = Signal(
	providing_args = [
		"user",
	]
)

workout_regeneration = Signal(
	providing_args = [
		"user"
	]
)

specific_diet_regeneration = Signal(
    providing_args = [
        "user",
        "week",
        "year"
    ]
)
