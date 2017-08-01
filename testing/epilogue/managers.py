from django.db import models


class Default(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(calarie__gt = 0)

class M1(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(m1 = '1').filter(calarie__gt = 0)

class M2(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(m2 = '1').filter(calarie__gt = 0)

class M3(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(m3 = '1').filter(calarie__gt = 0)

class M4(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(m4 = '1').filter(calarie__gt = 0)

class M5_Gain(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(m5_gain = '1').filter(calarie__gt = 0)

class M5_Loss(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(m5_loss = '1').filter(for_loss = 1).filter(calarie__gt = 0)

class M5_Stable(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(m5_stable = '1').filter(calarie__gt = 0)


class DayManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(day = self.day)


class Day1(DayManager):
	day = 1
class Day2(DayManager):
	day = 2
class Day3(DayManager):
	day = 3
class Day4(DayManager):
	day = 4
class Day5(DayManager):
	day = 5
class Day6(DayManager):
	day = 6
class Day7(DayManager):
	day = 7