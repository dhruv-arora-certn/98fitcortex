import random
import math
import itertools
import functools


def alternate_gen(iterable):
	cycled = itertools.cycle(iterable)
	while True:
		yield next(cycled)

def alternate_even():
	gen = alternate_gen([1,0])
	while True:
		yield next(gen)

def alternate_odd():
	gen = alternate_gen([0,1])
	while True:
		yield next(gen)

def walk_even(iterable):
	even_selector = alternate_even()
	compressed = itertools.compress(iterable , even_selector)
	return compressed

def walk_odd(iterable):
	odd_selector = alternate_odd()
	compressed = itertools.compress(iterable , odd_selector)
	return compressed
