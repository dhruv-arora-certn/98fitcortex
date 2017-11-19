import random
import math
import itertools
import functools


def alternate_gen(iterable):
	cycled = itertools.cycle(iterable)
	while True:
		yield next(cycled)

def alternate_even():
	pass

def walk_even(iterable):
	even_selector = generate_even(iterable)

