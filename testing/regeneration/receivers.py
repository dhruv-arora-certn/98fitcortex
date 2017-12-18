from django.dispatch import receiver

from .signals import diet_regeneration

@receiver(diet_regeneration)
def diet_regenerator(sender , *args , **kwargs):
	user = kwargs.pop('user')

