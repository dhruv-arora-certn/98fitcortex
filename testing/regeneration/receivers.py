from django.dispatch import receiver

from .signals import diet_regeneration
from .utils import get_window_tuples

import epilogue.constants

import logging

@receiver(diet_regeneration)
def diet_regenerator(sender , *args , **kwargs):
	user = kwargs.pop('user')
	logger = logging.getLogger(__name__)
	logger.debug("Received Diet Regeneration")
	eligible_window = get_window_tuples()

